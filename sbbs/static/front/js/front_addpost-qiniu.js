/**
 * Created by K_God on 2017/6/3.
 */

// // 初始化编辑器
// $(function () {
//     var editor = new wangEditor('editor');
//     editor.config.mapAk = 'hTfOjBGNnapTHyjGAHnooEpQ5TDeG4gP';  // 此处换成自己申请的密钥
//     editor.create();
//     window.editor = editor; //全球变量
// });


// 七牛，文本框编辑上传。
//$(function () {
//    var domain = 'http://oqwrm9r74.bkt.clouddn.com/';
//    var progressBox = $('#progress-box');
//    var progressBar = progressBox.children(0);
//    var uploadBtn = $('#upload-btn');
//    var submitBtn = $('#submit');
//    var uploader = Qiniu.uploader({
//           runtimes: 'html5,flash,html4',      // 上传模式，依次退化
//            browse_button: 'upload-btn',         // 上传选择的点选按钮，必需
//            // 在初始化时，uptoken，uptoken_url，uptoken_func三个参数中必须有一个被设置
//            // 切如果提供了多个，其优先级为uptoken > uptoken_url > uptoken_func
//            // 其中uptoken是直接提供上传凭证，uptoken_url是提供了获取上传凭证的地址，如果需要定制获取uptoken的过程则可以设置uptoken_func
//            // uptoken : '<Your upload token>', // uptoken是上传凭证，由其他程序生成
//            uptoken_url: '/qiniu_token',         // Ajax请求uptoken的Url，强烈建议设置（服务端提供）
//            // uptoken_func: function(file){    // 在需要获取uptoken时，该方法会被调用
//            //    // do something
//            //    return uptoken;
//            // },
//            get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的uptoken
//            // downtoken_url: '/downtoken',
//            // Ajax请求downToken的Url，私有空间时使用，JS-SDK将向该地址POST文件的key和domain，服务端返回的JSON必须包含url字段，url值为该文件的下载地址
//            unique_names: true,              // 默认false，key为文件名。若开启该选项，JS-SDK会为每个文件自动生成key（文件名）
//            // save_key: true,                  // 默认false。若在服务端生成uptoken的上传策略中指定了sava_key，则开启，SDK在前端将不对key进行任何处理
//            domain: domain,     // bucket域名，下载资源时用到，必需
//            // container: 'container',             // 上传区域DOM ID，默认是browser_button的父元素
//            max_file_size: '500mb',             // 最大文件体积限制
//            // flash_swf_url: 'path/of/plupload/Moxie.swf',  //引入flash，相对路径
//            max_retries: 3,                     // 上传失败最大重试次数
//           dragdrop: true,                     // 开启可拖曳上传
//            drop_element: 'editor-box',          // 拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
//            chunk_size: '4mb',                  // 分块上传时，每块的体积
//            auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传
//            //x_vars : {
//            //    查看自定义变量
//            //    'time' : function(up,file) {
//            //        var time = (new Date()).getTime();
//                      // do something with 'time'
//            //        return time;
//            //    },
//            //    'size' : function(up,file) {
//            //        var size = file.size;
//                      // do something with 'size'
//           //        return size;
//            //    }
//           //},
//          init: {
//             'FilesAdded': function(up, files) {
//                plupload.each(files, function(file) {
//                   // 文件添加进队列后，处理相关的事情
//                        });
//               },
//                'BeforeUpload': function(up, file) {
//                       // 每个文件上传前，处理相关的/事情
//                    uploadBtn.button('loading');
//                },
//                'U/ploadProgress': function(up, file) {
//                       // 每个文件上传时，处理相关的事情
//                    var percent = file.percent;
//                    progressBar.attr('aria-valuenow', percent);
//                    progressBar.css('width', percent+'%');
//                    progressBar.text(percent+'%');
//                },
//                'FileUploaded': function(up, file, info) {
//                       // 每个文件上传成功后，处理相关的事情
//                       // 其中info是文件上传成功后，服务端返回的json，形式如：
//                       // {
//                       //    "hash": "Fh8xVqod2MQ1mocfI4S4KpRL6D98",
//                       //    "key": "gogopher.jpg"
//                       //  }
//                       // 查看简单反馈
//                       // var domain = up.getOption('domain');
//                       // var res = parseJSON(info);
//                       // var sourceLink = domain +"/"+ res.key; 获取上传成功后的文件的Url
//                   var fileUrl = domain + file.target_name;
//                   if(file.type.indexOf('video') >= 0){
//                        // 视频
//                        var videoTag = "<video width='640' height='480' controls><source src="+fileUrl+"></video>";
//                        window.editor.$txt.append(videoTag);
//                    }else{
//                        // 图片
//                        var imgTag = "<img src="+fileUrl+">";
//                        window.editor.$txt.append(imgTag);
//                    }
//                    setTimeout(function () {
//                    progressBar.attr('aria-valuenow', 0);
//                    progressBar.css('width', '0%');
//                    progressBar.text('');
//                    uploadBtn.button('reset');
//                    },300);
//
//                },
//                'Error': function(up, err, errTip) {
//                       //上传出错时，处理相关的事情
//                },
//                'UploadComplete': function() {
//                       //队列文件处理完毕后，处理相关的事情
//                },
//                'Key': function(up, file) {
//                    // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
//                    // 该配置必须要在unique_names: false，save_key: false时才生效
//
//                    var key = "";
//                    // do something with key here
//                    return key
//                }
//            }
//        });
//
//        // domain为七牛空间对应的域名，选择某个空间后，可通过 空间设置->基本设置->域名设置 查看获取
//
//        // uploader为一个plupload对象，继承了所有plupload的方法
//        return uploader;
//}
//);

// 发布帖子的执行事件
$(function () {
   $("#submit").click(function (event) {
       event.preventDefault();

       var titleInput = $('input[name=title]');
        var captchaInput = $('input[name=graph-captcha]');

       var title = titleInput.val();
       var board_id = $('.board-select').val();
       var content = window.editor.$txt.html();
       var graph_captcha = captchaInput.val();

       console.log(graph_captcha);
       xtajax.post({
           'url': '/add_post/',
           'data':{
               'title': title,
               'board_id': board_id,
               'content': content,
               'graph_captcha': graph_captcha
           },
           'success': function (data) {
               if(data['code'] == 200){
                   xtalert.alertConfirm({
                       'msg': '恭喜！帖子发表成功！',
                       'cancelText': '回到首页',
                       'confirmText': '再发一篇',
                       'cancelCallback': function () {
                           window.location = '/';
                       },
                       'confirmCallback': function () {
                           titleInput.val('');
                           window.editor.clear();
                           captchaInput.val('');
                           $('#graph-captcha-btn').click();
                       }
                   });
               }else{
                   xtalert.alertInfoToast(data['message']);
                   $('#graph-captcha-btn').click();
               }
           }
       })
   });
});












