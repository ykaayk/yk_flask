/**
 * Created by K_God on 2017/5/3.
 */

$(function () {
    $('#captcha-btn').click(function (event) {
        event.preventDefault();

        var email = $('input[name=email]').val();

        xtajax.get({
            'url': '/mail_captcha/',
            'data':{
                'email': email
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('恭喜！验证码发送成功！');
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            },
            'fail': function (error) {
                xtalert.alertNetworkError();
            }
        })
    });
});

$(function () {
   $('#submit').click(function (event) {
       event.preventDefault();

       var emailInput = $('input[name=email]');
       var captchaInput = $('input[name=captcha]');

       var email = emailInput.val();
       var captcha = captchaInput.val();

       xtajax.post({
           'url': '/resetmail/',
           'data': {
               'email': email,
               'captcha': captcha
           },
           'success': function (data) {
               if(data['code'] == 200){
                   emailInput.val('');
                   captchaInput.val('');
                   xtalert.alertSuccessToast('恭喜！邮箱修改成功！');
               }else{
                   xtalert.alertInfoToast(data['message']);
               }
           },
           'fail': function (error) {
               xtalert.alertNetworkError();
           }
       })
   });
});

