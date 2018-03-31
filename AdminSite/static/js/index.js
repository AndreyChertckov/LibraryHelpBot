$(function(){
    $("#users").click(user_event);
});
function user_event(event) {
    event.preventDefault();
    bar_user = "<div class='bar'><button class='btn btn-sm ' id ='unconfirmed'>Unconfirmed</button>\
    <button class='btn btn-sm' id ='patrons'>Patrons</button>\
    <button class='btn btn-sm' id ='librarians'>Librarians</button></div>";
    
    $(".main").html(bar_user);

    $("#unconfirmed").click(function(){
        $.post("/api/get_all_unconfirmed", {}, function(data, status){
            output_html = "<div class='container'><h3>Unconfirmed</h3><div class='row'><div id='prev' class = 'col-md-1'><button class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div><div class='col-md-1'><button id='search-btn' class='btn btn-sm'><span data-feather='search'></span></button></div></div>\
            <div class='table-responsive'>\
                <table class='table table-striped table-sm'>\
                    <thead>\
                        <tr>\
                            <th>Id</th>\
                            <th>Name</th>\
                            <th>Phone</th>\
                            <th>Address</th>\
                            <th>Status</th>\
                            <th></th>\
                        </tr>\
                    </thead>\
                    <tbody>";
            data.forEach(elem => {
                output_html += "<tr id = '"+ elem['id']+"'>";
                output_html += "<td>" + elem['id'] + "</td>";
                output_html += "<td>" + elem['name'] + "</td>";
                output_html += "<td>" + elem['phone'] + "</td>";
                output_html += "<td>" + elem['address'] + "</td>";
                output_html += "<td>" + elem['status'] + "</td>";
                output_html += "<td><button class='btn accept'><span data-feather='user-check'></span></button> \0 <button class='btn reject'><span data-feather='user-x'></span></button></td>";
            });
            output_html += "</tbody></table></div></div>";
            $(".main").html(output_html);
            
            $(".accept").click(function(){
                user_id_ = $(this).parent().parent().attr("id");
                $.post("/api/confirm_user",{user_id:user_id_},function(data,status){});
                $(this).parent().parent().remove();
                return;
            });
            $(".reject").click(function(){
                user_id_ = $(this).parent().parent().attr("id");
                $.post("/api/delete_user",{user_id:user_id_},function(data,status){});
                $(this).parent().parent().remove();
                return;
            });    
            $("#prev").click(user_event); 
            $("#search-btn").click(function(){
                search_request = $("#search").val();
                $.post("/api/get_user_by_name",{name:search_request},function(data,status){
                    $("tbody").empty()
                    temp = "<tr id = '"+ data['id']+"'>";
                    temp += "<td>" + data['id'] + "</td>";
                    temp += "<td>" + data['name'] + "</td>";
                    temp += "<td>" + data['phone'] + "</td>";
                    temp += "<td>" + data['address'] + "</td>";
                    temp += "<td>" + data['status'] + "</td>";
                    temp += "<td><button class='btn accept'><span data-feather='user-check'></span></button> \0 <button class='btn reject'><span data-feather='user-x'></span></button></td></tr>";
                    $("tbody").append(temp);
                    feather.replace();
                });
                
            });
            feather.replace();   
        });
        return;
    });

    $("#patrons").click(function(){
        $.post("/api/get_all_patrons",{},function(data,status){
            output_html = "<div class='container'><h3>Patrons</h3><div class='row'><div class = 'col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div><div class='col-md-1'><button id='search-btn' class='btn btn-sm'><span data-feather='search'></span></button></div></div>\
            <div class='table-responsive'>\
                <table class='table table-striped table-sm'>\
                    <thead>\
                        <tr>\
                            <th>Id</th>\
                            <th>Name</th>\
                            <th>Phone</th>\
                            <th>Address</th>\
                            <th>Status</th>\
                            <th></th>\
                        </tr>\
                    </thead>\
                    <tbody>";
            data.forEach(elem => {
                output_html += "<tr id = '"+ elem['id']+"'>";
                output_html += "<td>" + elem['id'] + "</td>";
                output_html += "<td>" + elem['name'] + "</td>";
                output_html += "<td>" + elem['phone'] + "</td>";
                output_html += "<td>" + elem['address'] + "</td>";
                output_html += "<td>" + elem['status'] + "</td>";
                output_html += "<td><button class='btn info'><span data-feather='info'></span></button></td></tr>";
            });
            output_html += "</tbody></table></div>";
            $(".main").html(output_html);
            $("#prev").click(user_event);
            $("#search-btn").click(function(){
                search_request = $("#search").val();
                $.post("/api/get_user_by_name",{name:search_request},function(data,status){
                    $("tbody").empty()
                    temp = "<tr id = '"+ data['id']+"'>";
                    temp += "<td>" + data['id'] + "</td>";
                    temp += "<td>" + data['name'] + "</td>";
                    temp += "<td>" + data['phone'] + "</td>";
                    temp += "<td>" + data['address'] + "</td>";
                    temp += "<td>" + data['status'] + "</td>";
                    temp += "<td><button class='btn info'><span data-feather='info'></span></button></td></tr>";
                    $("tbody").append(temp);
                    feather.replace();
                    return;
                });
                return;
            });
            $(".info").click(user_info);
            feather.replace();
            return;
        });
        return;
    });
    $("#librarians").click(function(){
        $.post("/api/get_all_librarians",{},function(data,status){
            output_html = "<div class='container'><h3>Librarians</h3><div class='row'><div class = 'col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div><div class='col-md-1'><button id='search-btn' class='btn btn-sm'><span data-feather='search'></span></button></div></div>\
            <div class='table-responsive'>\
                <table class='table table-striped table-sm'>\
                    <thead>\
                        <tr>\
                            <th>Id</th>\
                            <th>Name</th>\
                            <th>Phone</th>\
                            <th>Address</th>\
                            <th></th>\
                        </tr>\
                    </thead>\
                    <tbody>";
            data.forEach(elem => {
                output_html += "<tr id = '"+ elem['id']+"'>";
                output_html += "<td>" + elem['id'] + "</td>";
                output_html += "<td>" + elem['name'] + "</td>";
                output_html += "<td>" + elem['phone'] + "</td>";
                output_html += "<td>" + elem['address'] + "</td></tr>";
            });
            output_html += "</tbody></table></div>";
            $(".main").html(output_html);
            $("#prev").click(user_event);
            $("#search-btn").click(function(){
                search_request = $("#search").val();
                $.post("/api/get_librarian_by_name",{name:search_request},function(data,status){
                    console.log(status);
                    console.log(data);
                    $("tbody").empty()
                    temp = "<tr id = '"+ data['id']+"'>";
                    temp += "<td>" + data['id'] + "</td>";
                    temp += "<td>" + data['name'] + "</td>";
                    temp += "<td>" + data['phone'] + "</td>";
                    temp += "<td>" + data['address'] + "</td>";
                    $("tbody").append(temp);
                    return;
                });
            });
            feather.replace();
            return;
        });
        return;
    });
}

function user_info() {
    user_id_ = 0;
    if($("#id").length){
        user_id_ = $("#id").html();
        console.log(user_id_);
    }else{
        user_id_ = $(this).parent().parent().attr('id');
    }
    $.post("/api/get_user",{user_id:user_id_},function(data,status){
        output_html_ = "<div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><h3 id='name'>"+data['name']+"</h3></div><div class='col-md-1'><button id = '"+user_id_+"' class='btn btn-sm settings'><span data-feather='settings'></span></div></div>\
        <h5>Id: </h5><p id='id'>" + data['id']+"</p>\
        <h5>Phone: </h5><p id='phone'>" + data['phone'] + "</p>\
        <h5>Address: </h5><p id='address'>"+data['address']+"</p>\
        <h5>Status: </h5><p id='status'>" + data['status']+"</p>\
        <h5>Current documents: </h5>";
        $.post("/api/get_user_orders",{user_id:user_id_},function(data,status){
            console.log(data);
            output_html_ += "<div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                    <tr>\
                        <th>Title</th>\
                        <th>Authors</th>\
                        <th>Type</th>\
                        <th>Ordering time</th>\
                        <th>Return time</th>\
                    </tr>\
                </thead>\
                <tbody>";
            data.forEach(elem => {
                output_html_ += "<tr id = '"+ elem['id']+"'>";
                output_html_ += "<td>" + elem['doc']['title'] + "</td>";
                output_html_ += "<td>" + elem['doc']['authors'] + "</td>";
                output_html_ += "<td>" + elem['table'] + "</td>";
                output_html_ += "<td>" + elem['time'] + "</td>";
                output_html_ += "<td>" + elem['time_out'] + "</td></tr>";
            });
            output_html_ += "</tbody></table>";
            output_html_ += "<h5> User history </h5>";
            output_html_ += "<div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                    <tr>\
                        <th>Title</th>\
                        <th>Authors</th>\
                        <th>Type</th>\
                        <th>Ordering time</th>\
                        <th>Return time</th>\
                    </tr>\
                </thead>\
                <tbody>";
            $.post("/api/get_user_history",{user_id:user_id_},function(data,status){
                data.forEach(elem => {
                    output_html_ += "<tr id = '"+ elem['id']+"'>";
                    output_html_ += "<td>" + elem['doc']['title'] + "</td>";
                    output_html_ += "<td>" + elem['doc']['authors'] + "</td>";
                    output_html_ += "<td>" + elem['table'] + "</td>";
                    output_html_ += "<td>" + elem['time'] + "</td>";
                    output_html_ += "<td>" + elem['time_out'] + "</td></tr>";
                });
                output_html_ += "</tbody></table>";
                $(".main").html(output_html_);
                $(".settings").click(modify_user);
                $("#prev").click(user_event);
                feather.replace();
            });
        });
    });
}

function modify_user() {
    user = {id:$("#id").html(),name:$("#name").html(),phone:$("#phone").html(),address:$("#address").html(),status:$("#status").html()};
    $(".main").empty();
    output_html = "<div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><h3>"+user['name']+"</h3></div></div>\
    Name: <input id='name' name='name' value='"+user['name']+"' type='text'></br>\
    Phone: <input id='phone' name='phone' value='"+user['phone']+"' type='text'></br>\
    Address: <input id='address' name='address' value='"+user['address']+"' type='text'></br>\
    Status: <input id='status' name='status' value='"+user['status']+"' type='text'></br>\
    <button id='save' class='btn'>Save</button>\
    <p hidden id='id'>"+user['id']+"</p>";
    $(".main").html(output_html);
    $("#save").click(function(event){
        event.stopImmediatePropagation();
        send_data = {id:user['id'],name:$("#name").val(),phone:$("#phone").val(),address:$("#address").val(),status:$("#status").val()};
        console.log(send_data)
        $.post("/api/modify_user",send_data,function(data,status){
            user_info();
        });
    });
    $("#prev").click(user_info);
    feather.replace();
}