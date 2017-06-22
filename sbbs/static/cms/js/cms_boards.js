/**
 * Created by K_God on 2017/5/30.
 */

$(function () {
    $('#add-board-btn').click(function (event) {
        event.preventDefault();
        xtalert.alertOneInput({
            'title': '添加新板块',
            'confirmCallback': function (inputValue) {
                xtajax.post({
                    'url': '/add_board/',
                    'data': {
                        'board_name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            xtalert.alertSuccessToast('恭喜！板块添加成功！');
                            setTimeout(function () {
                                window.location.reload();
                            }, 600);
                        }else {
                            xtalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        });
    });
});

// 编辑板块
$(function () {
    $('.edit-board-btn').click(function (event) {
        event.preventDefault();
        var board_id = $(this).attr('board-id');
        // console.log(board_id);
        xtalert.alertOneInput({
            'title': '编辑板块名称',
            'confirmCallback': function (inputValue) {
                xtajax.post({
                    'url': '/edit_board/',
                    'data': {
                        'board_id': board_id,
                        'board_name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            xtalert.alertSuccessToast('恭喜！修改板块名称成功！');
                            setTimeout(function () {
                                window.location.reload();
                            },600)
                        }else {
                            xtalert.alertInfoToast(data['message']);
                        }
                    }
                });
            }
        });
    });
});

// 删除板块
$(function () {
    $('.del-board-btn').click(function (event) {
        event.preventDefault();
        var board_id = $(this).attr('board-id');
        var board_name = $(this).attr('board-name');
        xtalert.alertConfirm({
            'title': '是否删除板块 ' + board_name + '?',
            'confirmText': '删除',
            'cancelText': '取消',
            'confirmCallback': function () {
                xtajax.post({
                    'url': '/del_board/',
                    'data': {
                        'board_id': board_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            var mes = board_name + ' 板块删除成功';
                            xtalert.alertSuccessToast(mes);
                            setTimeout(function () {
                                window.location.reload();
                            }, 600)
                        }else {
                            setTimeout(function () {
                                xtalert.alertInfoToast(data['message']);
                            }, 400);

                        }
                    }
                });
            }
        });
    });
});









