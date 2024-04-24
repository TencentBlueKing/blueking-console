BKNOTICE = (function () {
    var alertNoticeIndex = 0
    var alertNoticeList = [
        { content: '<span style="background-color: red">aaa</span>' },
        { content: 'bbb' }
    ]
    return {
        init: function () {
            BKNOTICE.get();
        },
        get: function(){
            // 获取通知信息
            $.ajax({
                type: "GET",
                data: {},
                url: urlPrefix + 'notice/announcements/',
                dataType: "json",
                xhrFields: { withCredentials: true },
                success: function (data) {
                    alertNoticeList = data?.data?.filter(item => item.announce_type === 'announce') || []

                    // 展示跑马灯公告
                    if (alertNoticeList.length > 0) {
                        $('.bk-notice-component-alert').css('display', 'flex')
                        var contentHeight = window.innerHeight - 40
                        $('#desktop').height(contentHeight)
                        BKNOTICE.changeAlertNoticeContent()
                    }
                    // 展示切换公告分页器
                    if (alertNoticeList.length > 1) {
                        $('.alert-notice-pagination').show()
                        $('.alert-notice-num').text((alertNoticeIndex + 1) + '/' + alertNoticeList.length)
                        if (alertNoticeIndex <= 0) {
                            $('.alert-prev-icon').addClass('icon-disabled')
                        }
                        if (alertNoticeIndex >= alertNoticeList.length - 1) {
                            $('.alert-next-icon').addClass('icon-disabled')
                        }
                    }
                },
                error: function (err) {
                    console.log('notice center error: ', err);
                }
            });
        },
        // 切换上一条或下一条公告
        changeAlertNoticeIndex : function(type){
            if (type === 'prev') {
                if (alertNoticeIndex > 0) {
                    alertNoticeIndex--
                }
            } else if (type === 'next') {
                if (alertNoticeIndex < alertNoticeList.length - 1) {
                    alertNoticeIndex++
                }
            }
            $('.alert-prev-icon').removeClass('icon-disabled')
            $('.alert-next-icon').removeClass('icon-disabled')
            if (alertNoticeIndex <= 0) {
                $('.alert-prev-icon').addClass('icon-disabled')
            }
            if (alertNoticeIndex >= alertNoticeList.length - 1) {
                $('.alert-next-icon').addClass('icon-disabled')
            }
            BKNOTICE.changeAlertNoticeContent()
        },

        // 展示当前公告内容， 过滤xss
        changeAlertNoticeContent : function(){
            var currentNotice = alertNoticeList[alertNoticeIndex] || ''

            const allowUriConfig = /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp|wxwork):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i;
            var showContent = DOMPurify.sanitize(currentNotice.content, {
                ALLOWED_URI_REGEXP: allowUriConfig
            })
            $('.bk-notice-content').html(showContent)
        },
        // 关闭跑马灯
        closeAlertNotice: function(){
            $('.bk-notice-component-alert').css('display', 'none')
            $('#desktop').height(window.innerHeight)
        },
    }
})();



