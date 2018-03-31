$(function(){
    $("#users").click(user_event);
    $("#documents").click(documents_event);
});

function user_event(event) {
    event.preventDefault();
    bar_user = "<div class='row'><div class ='col-10 content'></div><div class='col-2 sidebar-wrapper'><ul class='sidebar-nav'><li><button class='btn btn-sm ' id ='unconfirmed'>Unconfirmed</button></li>\
    <li><button class='btn btn-sm' id ='patrons'>Patrons</button></li>\
    <li><button class='btn btn-sm' id ='librarians'>Librarians</button></li></ul></div></div>";
    $(".main").html(bar_user);
    unconfirmed_table();
    $("#unconfirmed").click(unconfirmed_table);
    $("#patrons").click(patrons_table);
    $("#librarians").click(librarians_table);
}

function unconfirmed_table(){
    $.post("/api/get_all_unconfirmed", {}, function(data, status){
        output_html = "<h3>Unconfirmed</h3><div class='row'><div class='col-md-11'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div><div class='col-md-1'><button id='search-btn' class='btn btn-sm'><span data-feather='search'></span></button></div></div>\
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
        output_html += "</tbody></table></div>";
        $(".content").html(output_html);
        
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
}

function patrons_table(){
    $.post("/api/get_all_patrons",{},function(data,status){
        output_html = "<h3>Patrons</h3><div class='row'><div class='col-md-11'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div><div class='col-md-1'><button id='search-btn' class='btn btn-sm'><span data-feather='search'></span></button></div></div>\
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
        $(".content").html(output_html);
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
}

function librarians_table(){
    $.post("/api/get_all_librarians",{},function(data,status){
        output_html = "<h3>Librarians</h3><div class='row'><div class='col-md-11'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div><div class='col-md-1'><button id='search-btn' class='btn btn-sm'><span data-feather='search'></span></button></div></div>\
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
        $(".content").html(output_html);
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
                $(".content").html(output_html_);
                $(".settings").click(modify_user);
                $("#prev").click(patrons_table);
                feather.replace();
            });
        });
    });
}

function modify_user() {
    user = {id:$("#id").html(),name:$("#name").html(),phone:$("#phone").html(),address:$("#address").html(),status:$("#status").html()};
    output_html = "<div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><h3>"+user['name']+"</h3></div></div>\
    Name: <input id='name' name='name' value='"+user['name']+"' type='text'></br>\
    Phone: <input id='phone' name='phone' value='"+user['phone']+"' type='text'></br>\
    Address: <input id='address' name='address' value='"+user['address']+"' type='text'></br>\
    Status: <input id='status' name='status' value='"+user['status']+"' type='text'></br>\
    <button id='save' class='btn'>Save</button>\
    <p hidden "+data['best_seller']+"</p>id='id'>"+user['id']+"</p>";
    $(".content").html(output_html);
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

function documents_event(event){
    event.preventDefault();
    bar_user = "<div class='row'><div class ='col-10 content'></div><div class='col-2 sidebar-wrapper'><ul class='sidebar-nav'><li><button class='btn btn-sm ' id ='books'>Books</button></li>\
    <li><button class='btn btn-sm' id ='av_materials'>AV Materials</button></li>\
    <li><button class='btn btn-sm' id ='articles'>Articles</button></li></ul></div></div>";
    $(".main").html(bar_user);
    books();
    $("#books").click(books);
}

function books(){
    $.post("/api/get_all_doctype",{type:'book'},function(data,status){
        output_html = "<div class='row'>\
        <div class = 'col-2'><h3>Books</h3></div>\
        <div class='col-1'><button class='btn btn-sm add'><span data-feather='plus'></span></button></div>\
        </div>\
        <div class='row'><div class='col-md-11'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div><div class='col-md-1'><button id='search-btn' class='btn btn-sm'><span data-feather='search'></span></button></div></div>\
        <div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                    <tr>\
                        <th>Title</th>\
                        <th>Authors</th>\
                        <th>Count</th>\
                        <th>Free count</th>\
                        <th>Bestseller</th>\
                        <th></th>\
                    </tr>\
                </thead>\
                <tbody>";
        console.log(data);
        data.forEach(elem => {
            output_html += "<tr id = '"+ elem['id']+"'>";
            output_html += "<td>" + elem['title'] + "</td>";
            output_html += "<td>" + elem['authors'] + "</td>";
            output_html += "<td>" + elem['count'] + "</td>";
            output_html += "<td>" + elem['free_count'] + "</td>";
            if(elem['best_seller'] == 0) {
                output_html += "<td><span data-feather='x'></span></td>";
            }else{
                output_html += "<td><span data-feather='check'></span></td>";
            }
            output_html += "<td><button class='btn info'><span data-feather='info'></span></button></td></tr>";
        });
        output_html += "</tbody></table></div>";
        $(".content").html(output_html);
        $(".info").click(book_info);
        $(".add").click(edit_book);
        feather.replace();
        return;
    });
    return;
}

function book_info(){
    console.log('blet');
    book_id_ = 0;
    if($("#id").length){
        book_id_ = $("#id").html();
    }else{
        book_id_ = $(this).parent().parent().attr('id');
    }
    console.log(book_id_);
    $.post("/api/get_document",{id:book_id_,type:'book'},function(data,status){
        console.log(data);
        output_html_ = "<p id='id' hidden>"+book_id_+"</p><div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-9'><h3 id='title'>"+data['title']+"</h3></div><div class='col-md-1'><button class='btn btn-sm delete'><span data-feather='trash-2'></span></button></div><div class='col-md-1'><button id = '"+book_id_+"' class='btn btn-sm settings'><span data-feather='settings'></span></div></div>\
        <h5>Authors: </h5><p id='authors'>" + data['authors']+"</p>\
        <h5>Description: </h5><p id='description'>" + data['description'] + "</p>\
        <h5>Count: </h5><p id='count'>"+data['count']+"</p>\
        <h5>Free count: </h5><p id='free_count'>" + data['free_count']+"</p>\
        <h5>Price: </h5><p id='price'>" + data['price']+"</p>\
        <h5>Keywords: </h5><p id='keywords'>" + data['keywords']+"</p>\
        <p id='best_seller' hidden>"+data['best_seller']+"</p>";
        if(data['best_seller'] == 0) {
            output_html_ += "<h5>Best seller: <span data-feather='x'></span></h5>";
        }else{
            output_html_ += "<h5>Best seller: <span data-feather='check'></span></h5>";
        }
        if(data['queue'] != "[]"){ // TODO: display queue

        }
        $(".content").html(output_html_);
        $("#prev").click(books);
        $(".settings").click(edit_book);
        $(".delete").click(delete_book);
        feather.replace();
    });
}


function edit_book(){
    if($(this).attr('id')){
        book = {id:$(this).attr('id'),title:$("#title").html(),authors:$("#authors").html(),description:$("#description").html(),count:$("#count").html(),free_count:$("#free_count").html(),price:$("#price").html(),best_seller:$("#best_seller").html(),keywords:$("#keywords").html()};
        new_book = false;
    }else {
        book = {id:'',title:'New Book',authors:'',description:'',count:'',free_count:'',price:'',best_seller:'',keywords:''};
        new_book = true;
    }
    output_html = "<div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><h3>"+book['title']+"</h3></div></div>\
    Title: <input id='title' name='title' value='"+book['title']+"' type='text'></br>\
    Authors: <input id='authors' name='authors' value='"+book['authors']+"' type='text'></br>\
    Description: <textarea id='description' name='description'>"+book['description']+"</textarea></br>\
    Count: <input id='count' name='count' value='"+book['count']+"' type='text'></br>\
    Free count: <input id='free_count' name='free_count' value='"+book['free_count']+"' type='text'></br>\
    Price: <input id='price' name='price' value='"+book['price']+"' type='text'></br>\
    Best seller: <input id='best_seller' name='best_seller' value='"+book['best_seller']+"' type='text'></br>\
    Keywords: <input id='keywords' name='keywords' value='"+book['keywords']+"' type='text'></br>\
    <button id='save' class='btn'>Save</button><p id='id' hidden>"+book['id']+"</p>";
    $(".content").html(output_html);
    $("#save").click(function(event){
        event.stopImmediatePropagation();
        send_data = book = {id:$("#id").html(),title:$("#title").val(),authors:$("#authors").val(),description:$("#description").val(),count:$("#count").val(),free_count:$("#free_count").val(),price:$("#price").val(),best_seller:$("#best_seller").val(),keywords:$("#keywords").val(),type:'book'};
        console.log(send_data);
        if(new_book){
            $.post("/api/add_document",send_data,function(data,status){
                books();
            });
        }else{
            $.post("/api/modify_document",send_data,function(data,status){
                book_info();
            });
        }
    });
    if(new_book){
        $("#prev").click(books);
    }else{
        $("#prev").click(book_info);
    }

    feather.replace();
}

function delete_book(){
    book_id_ = $("#id").html();
    $.post("/api/delete_document",{id:book_id_,type:'book'},function(data,status){
        books();
    });
}

function av_materials(){

}

function articles() {

}