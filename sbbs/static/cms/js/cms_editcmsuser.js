/**
 * Created by K_God on 2017/5/16.
 */

$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();

        var checkedInputs = $(':checkbox:checked');

        var roles = [];
        // 遍历
        checkedInputs.each(function () {
            var role_id = $(this).val();
            roles.push(role_id);  // 添加到数组roles中

        // 拿到所有roles的id
        });

        var user_id = $(this).attr('data-user-id');
        xtajax.post({
            'url': '/edit_cmsuser/',
            'data': {
                'user_id': user_id,
                'roles': roles
            },
            'success': function (data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('恭喜！CMS用户信息修改成功！')
                }else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        })
    });
});

$(function () {
    $('#black-list-btn').click(function (event) {
        event.preventDefault();
        var user_id = $(this).attr('data-user-id');
        var is_active = !(!parseInt($(this).attr('data-is-active')));

        // var is_black;
        // (is_active==1 )? is_black=true : is_black=false;

        xtajax.post({
            'url': '/black_list/',
            'data': {
                'user_id': user_id,
                // 'is_black': is_black
                'is_black': is_active
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    // if(is_black){
                    if(is_active){
                        msg = '恭喜！已将该用户拉入黑名单！'
                    }else{
                        msg = '恭喜！已将该用户移出黑名单！'
                    }
                    xtalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload();
                    }, 600);
                }else {
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});