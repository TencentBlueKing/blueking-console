# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - 蓝鲸桌面 (BlueKing - bkconsole) available.
Copyright (C) 2022 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.

We undertake not to change the open source license (MIT license) applicable

to the current version of the project delivered to anyone in the future.
"""
import json
import re

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django_prometheus.middleware import PrometheusAfterMiddleware

from common.log import logger
from common.utils.xss.escape_function import html_escape, texteditor_escape, url_escape


class CheckXssMiddleware(MiddlewareMixin):
    """
    XSS攻击统一处理中间件
    """

    def process_view(self, request, view, args, kwargs):
        """
        请求参数统一处理
        """
        try:
            # 判断豁免权
            if getattr(view, "escape_exempt", False):
                return None
            # 判断豁免
            escape_type = None
            if getattr(view, "escape_texteditor", False):
                escape_type = "texteditor"
            elif getattr(view, "escape_url", False):
                escape_type = "url"
            # get参数转换
            request.GET = self.__escape_data(request.path, request.GET, escape_type)
            # post参数转换
            request.POST = self.__escape_data(request.path, request.POST, escape_type)
        except Exception as e:
            logger.error("CheckXssMiddleware Conversion failed! Error message: %s" % e)
        return None

    def __escape_data(self, path, query_dict, escape_type=None):  # noqa
        """
        GET/POST参数转义
        """
        data_copy = query_dict.copy()
        for _get_key, _get_value_list in data_copy.lists():
            new_value_list = []
            for _get_value in _get_value_list:
                new_value = _get_value
                # json串不进行转义
                try:
                    json.loads(_get_value)
                    is_json = True
                except Exception:
                    is_json = False
                # 转义新数据
                if not is_json:
                    try:
                        if escape_type is None:
                            use_type = self.__filter_param(path, _get_key)
                        else:
                            use_type = escape_type
                        if use_type == "url":
                            new_value = url_escape(_get_value)
                        elif use_type == "texteditor":
                            new_value = texteditor_escape(_get_value)
                        else:
                            new_value = html_escape(_get_value)
                    except Exception as e:
                        logger.error("CheckXssMiddleware GET/POST Parameters conversion failed: %s" % e)
                        new_value = _get_value
                else:
                    try:
                        new_value = html_escape(_get_value, True)
                    except Exception as e:
                        logger.error("CheckXssMiddleware GET/POST Parameters conversion failed: %s" % e)
                        new_value = _get_value
                new_value_list.append(new_value)
            data_copy.setlist(_get_key, new_value_list)
        return data_copy

    def __filter_param(self, path, param):
        """
        特殊path处理
        @param path: 路径
        @param param: 参数
        @return: 'url/texteditor'
        """
        use_url_paths, use_texteditor_paths = self.__filter_path_list()
        result = self.__check_escape_type(path, param, use_url_paths, "url")
        # 富文本内容过滤
        if result == "html":
            result = self.__check_escape_type(path, param, use_texteditor_paths, "texteditor")
        return result

    def __check_escape_type(self, path, param, check_path_list, escape_type):
        """
        判断过滤类型
        @param path: 请求Path
        @param param: 请求参数
        @param check_path_list: 指定类型Path列表
        @param escape_type: 判断过滤类型
        @param result_type: 结果类型
        """
        try:
            result_type = "html"
            for script_path, script_v in list(check_path_list.items()):
                is_path = re.match(r"^%s" % script_path, path)
                if is_path and param in script_v:
                    result_type = escape_type
                    break
        except Exception as e:
            logger.error("CheckXssMiddleware Special path processing failed! Error message: %s" % e)
        return result_type

    def __filter_path_list(self):
        """
        特殊path注册
        注册格式：{'path1': [param1, param2], 'path2': [param1, param2]}
        """
        use_url_paths = {
            "%saccounts/login" % settings.SITE_URL: ["c_url"],
            "%s" % settings.SITE_URL: ["url"],
        }
        use_texteditor_paths = {}
        return (use_url_paths, use_texteditor_paths)


class PrometheusAfterWithExclusionMiddleware(PrometheusAfterMiddleware, MiddlewareMixin):
    """自定义指标中间件，排除特定路径的指标统计"""

    def process_response(self, request, response):
        """处理响应时跳过指定路径"""
        # 排除 /console/ping/ 和 /console/healthz/ 路径的 Metric 指标统计
        if request.path in ['/console/ping/', '/console/healthz/']:
            return response
        return super().process_response(request, response)
