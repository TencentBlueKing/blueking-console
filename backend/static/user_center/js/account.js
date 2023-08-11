//点击修改个人信息
$('.from-content #modify-info').on('click',function(){
    var type = $(this).attr('data-type');
    $("#error_tip").text('');
    if(type == 'modify'){
        $('.editor-content').find('.from-content input').addClass('br');
        $('.editor-content').find('.from-content input').removeAttr('disabled');
        $('.editor-content').find('.from-content input').each(function(i){
            $(this).attr('data', $(this).val());
            if($(this).val() == '--'){
                $(this).val('');
            }
        });
        $(".other_operate").hide();
        $("#cancel-modify").show();
        $(this).attr('data-type', 'save');
        $(this).text(gettext('保存'));
    }else{
        var chname = $.trim($("#chname").val());
        if (!chname.match(/^[\u4e00-\u9fa5a-zA-Z0-9_]{1,16}$/)){
            $("#error_tip").html(gettext('中文名只能包含数字、字母、中文汉字、下划线，长度在1-16个字符'));
            $('#chname').focus();
            return false;
        }
        var phone = $.trim($("#phone").val());
        if (!phone.match(/^\d{10,11}$/)){
            $("#error_tip").text(gettext('仅支持中国大陆手机号码（11位数字）'))
            $('#phone').focus();
            return false;
        }
        var email = $.trim($("#email").val());
        if (!email.match(/^[A-Za-z0-9]+([-_.][A-Za-z0-9]+)*@([A-Za-z0-9]+[-.])+[A-Za-z0-9]{2,5}$/)){
            $("#error_tip").text(gettext('请输入正确的邮箱格式'))
            $('#email').focus();
            return false;
        }
        var qq = $.trim($("#qq").val());
        if (!qq.match(/^[1-9]\d{4,}$/)){
            $("#error_tip").text(gettext('仅支持合法的QQ号码'))
            $('#qq').focus();
            return false;
        }
        var url = site_url + 'user_center/account/modify_user_info/';
        $.post(url,{
            chname: chname,
            phone: phone,
            email: email,
            qq: qq
        },function(data){
            if(data.result){
                // 保存成功后刷新页面
                window.location.reload();
            }else{
                $("#error_tip").text(data.message);
            }
        }, 'json');
    }
  // $('.editor-content').find('.from-content input').focus();
});
// 取消用户信息修改
$('.from-content #cancel-modify').on('click', function(){
    $("#error_tip").text('');
    $('.editor-content').find('.from-content input').removeClass('br');
    $('.editor-content').find('.from-content input').attr('disabled', true);
    $('.editor-content').find('.from-content input').each(function(i){
        $(this).val($(this).attr('data'));
    });
    $(".other_operate").show();
    $("#cancel-modify").hide();
    $('#modify-info').attr('data-type', 'modify');
    $('#modify-info').text(gettext('修改个人信息'));
});
var change_password_html = [
    '<div>',
    '    <label class="password_label" style="width:80px;">' + gettext('新密码：') + '<span style="color:red">*</span> </label>',
    '    <!-- 防止Firefox下密码自动填充 -->',
    '    <input type="text" style="display:none">',
    '    <input type="password" style="display:none">',
    '    <input class="form-control password_input" style="width:250px" id="id_password1" name="password1"  type="text" onfocus="this.type=\'password\'">',
    '    <span style="color:red;display:none" class="error_tip ml10">' + gettext('必填') + '</span>',
    '    <p style="margin: 10px 0 10px 83px;" class="tip" id="pattern_tip">' + gettext('请输入密码，长度在8-20个字符，可支持数字、字母以及!@#$%^*()_-+=，必须保证密码包含大小写字母和数字') + '</p>',
    '</div>',
    '<div style="margin-bottom:10px;">',
    '    <label class="password_label" style="width:80px;">' + gettext('确认密码：') + '<span style="color:red">*</span> </label>',
    '    <input class="form-control password_input" style="width:250px" id="id_password2" name="password2" placeholder="' + gettext('再次输入密码') + '"  type="text" onfocus="this.type=\'password\'">',
    '    <span style="color:red;display:none" class="error_tip ml10">' + gettext('必填') + '</span>',
    '</div>',
    '<span id="password_tip" style="color:red;margin-left: 83px;"></span>',
].join('');
// 修改密码
$('#change-password').on('click', function(){
    $('.error_tip').hide();
    $(".password_input").val('');
    $("#password_tip").text('');
    art.dialog({
        id: "bktips",
        title:gettext("修改密码"),
        lock: true,
        width: 500,
        content: change_password_html,
        cancelVal: gettext("取消"),
        cancel: function(){
        },
        okVal: gettext("修改密码"),
        ok: function(){
            var flag = true;
            $('.error_tip').hide();
            $("#pattern_tip").css('color', '#887b7b');
            $(".password_input").each(function(){
                var curl_val = $.trim($(this).val());
                if(!curl_val){
                    $(this).next('.error_tip').show();
                    $(this).focus();
                    flag = false;
                    return false;
                }
                // 第一个密码需要验证格式
                if (!curl_val.match(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9!@#\$%\^\*\(\)-_\+=]{8,20}$/) && $(this).attr('name')=='password1'){
                    $("#pattern_tip").css('color', 'red');
                    $(this).focus();
                    flag = false;
                    return false;
                }
            });
            if(!flag){
                return false;
            }
            var password1 = $.trim($("#id_password1").val().trim());
            var password2 = $.trim($("#id_password2").val().trim());
            if(password1 != password2){
                $("#password_tip").text(gettext('两次输入的新密码不一致'));
                flag = false;
            }
            if(!flag){
                return false;
            }else{
                var url = site_url + 'user_center/account/change_password/';
                var post_flag = true;
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        'new_password1':password1,
                        'new_password2':password2,
                    },
                    success: function(data){
                        if(!data.result){
                            $("#password_tip").text(data.message);
                            post_flag = false;
                        }
                    },
                    dataType: 'json',
                    async: false,
                });
                // 出错则不关闭当前对话框
                if(!post_flag){
                    return false;
                }else{
                    art.dialog({width: 300,icon: 'succeed',lock: true,content: gettext('密码修改成功')}).time(2);
                    setTimeout(function(){
                        window.parent.BLUEKING.base.logout_handler();
                    }, 2100);
                }
            }
        }
    });
})
