/**
 * Created by K_God on 2017/5/27.
 */

$(function () {
    $('#black-list-btn').click(function (event) {
        event.preventDefault();

        var is_active = parseInt($(this).attr('data-is-active'));
        var user_id = $(this).attr('data-user-id');

        var is_black;
        (is_active == 1)? is_black=true: is_black=false ;

        xtajax.post({
            'url': '/black_front_user/',
            'data':{
                'user_id': user_id,
                'is_black': is_black
            },
            'success':function (data) {
                if(data['code'] == 200){
                    var message = '';
                    if(is_black){
                        message = '已经将该用户加入黑名单！';
                    }
                    else{
                        message = '已经将该用户移出黑名单！';
                    }
                    xtalert.alertInfoToast(message);
                    setTimeout(function () {
                         window.location.reload();
                    }, 500);
                }else{
                    xtalert.alertErrorToast(data['message']);
                    // xtalert.alertErrorToast('out');
                }
            }
        });
    });
});
