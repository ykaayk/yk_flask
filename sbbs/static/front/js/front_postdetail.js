/**
 * Created by K_God on 2017/6/11.
 */

// 计时器3s
$(function () {
    var timeSecend = 3;
    var post_id = $('#star-btn').attr('data-post-id');
    var timer = setInterval(function () {
        console.log(timeSecend);
        timeSecend --;
        if(timeSecend <= 0){
            clearInterval(timer);
            console.log(post_id);
            xtajax.post({
                'url': '/read_time/',
                'data':{
                'read_num': '1',
                'post_id': post_id
                },
            'success': function (data) {
                if(data['code'] == 200){
                    return null
                }else{
                    return null
                }
                }
            });
        }
    }, 1000);
});

// 提交评论的积分要求
$(function () {
    var commentPoints = 10;
   $('#comment-btn').click(function (event) {
       if($(this).attr('data-front-user-points') == null){
            console.log('hhh');
       }else if($(this).attr('data-front-user-points') < commentPoints ){
           event.preventDefault();
           var message = '你的积分是'+$(this).attr('data-front-user-points')+'分，请做任务来获取更多积分！';
           xtalert.alertErrorToast(message);
       }
   });
});

// 点赞
$(function () {
    $('#star-btn').click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var is_star = !(!parseInt($(this).attr('data-is-star')));
        xtajax.post({
            'url': '/post_star/',
            'data': {
                'post_id': post_id,
                'is_star': is_star
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var message = '';
                    if(is_star){
                         message='已取消点赞！'
                    }else{
                        message='已点赞！'
                    }
                    xtalert.alertSuccessToast(message);
                    setTimeout(function () {
                        window.location.reload()
                    }, 600);
                }
            }
        })
    })
});

// 发表评论的子评论
// 点开子评论框动画
$(function () {
    var replyBtn = $('.reply-btn');
    replyBtn.click(function (event) {
        event.preventDefault();
        var commentId = $(this).attr('data-comment-id');
        $('#comment-box-'+commentId).slideToggle('slow');
    });
});


// 提交子评论
$(function () {
    var btnCommentDouble = $('.btn-comment-double');
    btnCommentDouble.click(function (event) {
        event.preventDefault();
        var commentId = $(this).attr('data-comment-id');
        var commentDouble = $('#comment-text-'+commentId).val();
        xtajax.post({
            'url': '/comment_reply/',
            'data':{
                'comment_id': commentId,
                'reply': commentDouble
            },
            'success': function(data) {
                if(data['code'] == 200){
                    xtalert.alertSuccessToast('评论成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },300)
                }else{
                    xtalert.alertInfoToast(data['message']);
                }
            }
        });
    });
});

// 取消最后一个评论li的底栏
$(function () {
    $('.reply-ul').each(function () {
        $(this).children().last().attr('style', 'border-bottom: none;');
    })

});

