/**
 * Created by Administrator on 2017/7/5.
 */
var In = {
    CheckBlog : function (ttis) {
        ttis.addClass('checked')
    },
    SwitchStatus : function (id) {
        if($("#"+id).is(":visible")) {
            $("#"+id).slideUp();
        } else {
            $("#"+id).slideDown();
        }

    }
};