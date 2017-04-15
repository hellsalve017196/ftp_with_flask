$(document).ready(function () {

    var check_flag = true;

    var url = $("#url").html();

    $("#upload").on("click", function () {

        files = document.getElementById("datashak").files;

        if (files.length > 0) {

            var fd = new FormData();


            for(var i=0;i < files.length;i++) {
                var file = files[i];
                fd.append('datashak',file,file.name); // adding multiple files to one single name
            }


            var req = new XMLHttpRequest();

            req.upload.addEventListener("progress", upload_progress, false);
            req.upload.addEventListener("load", upload_complete, false);
            req.upload.addEventListener("error", upload_failed, false);
            req.upload.addEventListener("abort", upload_cancelled, false);

            http = url+"upload_datashak";

            req.open("POST",http,true);

            req.setRequestHeader("Cache-Control","no-cache");

            req.send(fd);

            check_flag = false;
        }

    });


    function upload_progress(evt) {
        $("#upload").hide();

        if (evt.lengthComputable) {
            var percentComplete = Math.round(evt.loaded * 100 / evt.total);

            $("#progress").show();

            $("#progress-bar").css({"width" : percentComplete.toString() + "%"})

        }
        else {
            $("#upload").show();
        }
    }


    function upload_complete(evt) {
        $("#progress").hide();
        $("#progress-bar").css({"width" : "0%"});

        $("#upload").show();

        check_flag = true;
    }


    function upload_failed(evt) {
        $("#progress").hide();
        $("#progress-bar").css({"width" : "0%"});

        console.log("Upload Failed for the server");
    }


    function upload_cancelled(evt) {
        console.log("Upload Cancelled")
    }


    var check_file_list = function() {
        if(check_flag) {

            $.ajax({
                method : 'GET',
                url : url + 'file_list',
                data : {},
                success : function(res) {
                    res = JSON.parse(res);
                    files = res.data;

                    str = '';

                    for(var i=0;i < files.length;i++) {
                        str += '<tr><td>'+files[i]+'</td><td><a href="'+url+'datashak/'+files[i]+'" target="_blank" class="btn btn-sm btn-primary">Download</a></td><td> <a target="_blank" class="btn btn-sm btn-danger" href="'+url+'file_delete/'+files[i]+'">Delete</a> </td></tr>';

                    }

                    $("#files").html(str);

                }
            })

        }
    };



    setInterval(check_file_list,3000);

    check_file_list();





});