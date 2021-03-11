function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function update_path_info(URL, path_info, block_id) {
    console.log('(func)update_path_info: ', URL, path_info, block_id);
    if(path_info.length === 0 || block_id.length === 0){
        console.log('Can\'t deal with 0 length shape/block_id! return');
        return;
    }
    let data = {
        'block_id': block_id,
        'road_info': JSON.stringify(path_info)
    };
    $.post(URL, data, function (response) {
        if (response === 'success') {
            path_info.length = 0;
            console.log(response);
        } else {
            console.log(response);
        }
        window.location.reload();
    });
}

function leave_mouse_tool() {
    mouseTool.close(true);
    path_info.length = 0;
}

function delete_seg(ev, URL) {
    console.log('func delete_seg: ', this.URL, ev.target.getExtData());
    path_info.length = 0;
    $.post(this.URL, {'seg_id': ev.target.getExtData()}, function (response) {
        if (response === 'success') {
            console.log(response);
            location.reload();
        } else {
            console.log(response);
        }
        window.location.reload();
    });
}
