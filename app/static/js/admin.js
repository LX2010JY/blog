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
    },
    addblog : function () {

    }
};
var btype = {
    num : 0,
    addOne : function () {
        var leng = $("#types").children().length;
        if(leng==btype.num) {
            $("#types").append('<li id="type_0" class="type" data-id="0"><input id="blog_type_upd_0" type="text" class="form-control" ' +
                'style="width: 125px;float: left" placeholder="填写类型名称" value=""><i onclick="btype.addType();return false;" class="layui-icon sure" style="position: relative;top:3px">&#xe618;</i><span class="delete" onclick="btype.removeOne(0)">&times;</span></li>');
            // btype.num++;
        } else {
            $("#blog_type_upd_0").focus();
        }
    },
    removeOne : function (id) {
        $("#type_"+id).addClass('remove');
        setTimeout(function () {
            $("#type_"+id).remove();
            btype.num--;
        },300);
        event.stopPropagation();
    },
    addType : function () {
        if($("#type_0").length<=0) return;
        var name = $("#blog_type_upd_0").val();
        if(!name) {
            // layer.alert('填写类型名称才可保存',{icon:2});
            // return;
            $("#blog_type_upd_0").focus();
            return;
        }
        layer.load();
        $.post('/admin/btype/add',{"name":name},function (dat) {
            layer.closeAll('loading');
            res = dat.split(':::');
            if(res[0]=='ok') {
                $("#blog_type_upd_0").attr('id','blog_type_upd_'+res[1]);
                $("#blog_type_upd_"+res[1]).hide();
                $("#type_0").attr('id','type_'+res[1]);
                $("#type_"+res[1]).prepend('<span id="blog_type_'+res[1]+'">'+name+'</span>');
                $("#type_"+res[1]+" .delete").attr('onclick','btype.removeType('+res[1]+')');
                $("#type_"+res[1]).attr('onclick','btype.checkType('+res[1]+')');
                btype.num++;
            } else {
                layer.alert('失败了:'+dat,{icon:3});
            }
        });
        event.stopPropagation();
    },
    removeType : function (id) {
        layer.load();
        $.post('/admin/btype/del',{"id":id},function (dat) {
            layer.closeAll('loading');
            if(dat=='ok') {
                btype.removeOne(id);
            } else {
                layer.alert('失败了：'+dat,{icon:3});
            }
        });
        event.stopPropagation();
    },
    checkType : function (id) {
        $("li.type").each(function (i,o) {
            $(this).removeClass('checked');
        });
        $("#type_"+id).addClass('checked');
        $("#btype").val(id);
        $("#btype_show").val($("#blog_type_"+id).text());
        $(".types").slideUp();
    }
}