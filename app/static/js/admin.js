/**
 * Created by yuan on 2017/7/4.
 */
var Ad = {
    editor : '',
    'createEditor' : function () {
        Ad.editor = new Simditor({
            textarea: $('#blog_body'),
            defaultImage: '/static/img/favicon.jpg',
            params: null,
            upload: {
                url: "/admin/uploadpic",
                connectionCount:3,
                leaveConfirm: '正在上传文件'
            },
            emoji:{
                imagePath: '/static/js/ext/simditor/emoji/images/emoji/'
            },
            tabIndent: true,
            toolbar : ['html','title','emoji','bold','underline','strikethrough','color','ol','ul','blockquote',
                'code','link','image','fullscreen'],
            toolbarFloat: true,
            pasteImage: true,
            allowedTags:['div','link','table','tr','td','br', 'span', 'a', 'img', 'b', 'strong', 'i', 'strike', 'u', 'font', 'p', 'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'h1', 'h2', 'h3', 'h4', 'hr'],
            allowedAttributes:{
                div:['class','style'],
                link:['href','rel'],
                img: ['src', 'alt', 'width', 'height', 'data-non-image'],
                a: ['href', 'target'],
                font: ['color'],
                code: ['class'],
            }
        });
    },
    ShowLaserBean : function () {
        $("#title_block").addClass('laser');
    },
    HideLaserBean : function () {
        $("#title_block").removeClass('laser');
    }
}