$(function(){
    $("#dashboard").click(dashboard);
    $("#users").click(user_event);
    $("#documents").click(documents_event);
    $("#orders").click(orders_event);
    $("#history").click(history_event);
});

function dashboard(event){
    event.preventDefault();
    bar_user = "<div class='row'><div class ='col-10 content'></div><div class='col-2 sidebar-wrapper'><ul class='sidebar-nav'><li><button class='btn btn-sm ' id ='invite_links'>Invite links</button></li>\
    <li><button class='btn btn-sm' id ='telegram'>Telegram</button></li></ul></div></div>";
    $(".main").html(bar_user);
    invite_links();
    $("#invite_links").click(invite_links);
    $("#telegram").click(telegram);
}

function invite_links(){
    $.post("/api/get_verification_links",{},function(data,status){
        output_html = "<div class='row'><div class='col-3'><h3>Invite links</h3></div><div class='col-1'><button class= 'btn btn-sm' id='add'><span data-feather='plus'></span></button></div></div>";
        output_html += "<h6>Send one of this links to librarian</h6>";
        data.forEach(elem => {
            output_html += elem + "</br>";
        });
        $(".content").html(output_html);
        feather.replace();
        $("#add").click(generate_link);
    });
}

function generate_link(){
    $.post("/api/generate_invite_link",{},function (data,status){
        invite_links();
    });
}

function telegram() {
    $.post("/api/get_telegram_verification_message",{},function(data,status){
        $(".content").html(data);
    });
}

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
        output_html = "<h3>Unconfirmed</h3><div class='row'><div class='col-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
        <div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                        <th>Id</th>\
                        <th>Name</th>\
                        <th>Phone</th>\
                        <th>Address</th>\
                        <th>Status</th>\
                        <th></th>\
                </thead>\
                <tbody id='tbody'>";
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
    
        });
        $(".reject").click(function(){
            user_id_ = $(this).parent().parent().attr("id");
            $.post("/api/delete_user",{user_id:user_id_},function(data,status){});
            $(this).parent().parent().remove();
    
        });
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
          });
        feather.replace();   
    });
}

function patrons_table(){
    $.post("/api/get_all_patrons",{},function(data,status){
        output_html = "<h3>Patrons</h3><div class='row'><div class='col-md-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
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
                <tbody id='tbody'>";
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
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
        $(".info").click(user_info);
        feather.replace();

    });
}

function librarians_table(){
    $.post("/api/get_all_librarians",{},function(data,status){
        output_html = "<h3>Librarians</h3><div class='row'><div class='col-md-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
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
                <tbody id='tbody'>";
        data.forEach(elem => {
            output_html += "<tr id = '"+ elem['id']+"'>";
            output_html += "<td>" + elem['id'] + "</td>";
            output_html += "<td>" + elem['name'] + "</td>";
            output_html += "<td>" + elem['phone'] + "</td>";
            output_html += "<td>" + elem['address'] + "</td></tr>";
        });
        output_html += "</tbody></table></div>";
        $(".content").html(output_html);
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
          });
        
        feather.replace();

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
        output_html_ = "<div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-9'><h3 id='name'>"+data['name']+"</h3></div><div class='col-md-1'><button class='btn btn-sm delete "+user_id_+"'><span data-feather='trash-2'></span></div><div class='col-md-1'><button id = '"+user_id_+"' class='btn btn-sm settings'><span data-feather='settings'></span></div></div>\
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
                $(".delete").click(delete_user);
                $("#prev").click(patrons_table);
                feather.replace();
            });
        });
    });
}

function delete_user(){
    user_id = $(this).attr("class").split(' ');
    user_id = user_id[user_id.length-1];
    console.log(user_id);
    $.post("/api/delete_user", {user_id:user_id},function (data,status){
        console.log(data);
        patrons_table();
    });
}

function modify_user() {
    user = {id:$("#id").html(),name:$("#name").html(),phone:$("#phone").html(),address:$("#address").html(),status:$("#status").html()};
    output_html = "<div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><h3>"+user['name']+"</h3></div></div>\
    <form>\
    <div class='form-group'>\
    <label for='name'>Name</lable></br>\
    <input type='form-control'id='name' name='name' value='"+user['name']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='phone'>Phone</lable></br>\
    <input type='form-control'id='phone' name='phone' value='"+user['phone']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='address'>Address</lable></br>\
    <input type='form-control'id='address' name='address' value='"+user['address']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='status'>Status</lable></br>\
    <input type='form-control'id='status' name='status' value='"+user['status']+"' type='text'>\
    </div>\
    <button id='save' class='btn'>Save</button>\
    <p id='id' hidden>"+user['id']+"</p>\
    </form>";
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
    $("#av_materials").click(av_materials);
    $("#articles").click(articles);
}

function books(){
    $.post("/api/get_all_doctype",{type:'book'},function(data,status){
        output_html = "<div class='row'>\
        <div class = 'col-2'><h3>Books</h3></div>\
        <div class='col-1'><button class='btn btn-sm add'><span data-feather='plus'></span></button></div>\
        </div>\
        <div class='row'><div class='col-md-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
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
                <tbody id='tbody'>";
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
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
          });
        
        feather.replace();

    });
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
        <div class='row'><div class='col-1'><h5>Count: </h5></div> <div class='col-1'><button id='add' class='btn btn-sm'><span data-feather='plus'></span></button> </div><div class='col-1'><button id='sub' class='btn btn-sm'><span data-feather='minus'></span></button></div></div><p id='count'>"+data['count']+"</p>\
        <h5>Free count: </h5><p id='free_count'>" + data['free_count']+"</p>\
        <h5>Price: </h5><p id='price'>" + data['price']+"</p>\
        <h5>Keywords: </h5><p id='keywords'>" + data['keywords']+"</p>\
        <p id='best_seller' hidden>"+data['best_seller']+"</p>";
        if(data['best_seller'] == 0) {
            output_html_ += "<h5>Best seller: <span data-feather='x'></span></h5>";
        }else{
            output_html_ += "<h5>Best seller: <span data-feather='check'></span></h5>";
        }
        if(data['queue'] != "[]"){ 
            $.post("/api/get_queue_on_document",{doc_id:book_id_,type:'book'},function(data,status){
                output_html_ += "<h5>Queue: </h5><div class='table-responsive'>\
                <table class='table table-striped table-sm'>\
                    <thead>\
                        <tr>\
                            <th>Name</th>\
                            <th>Status</th>\
                        </tr>\
                    </thead>\
                    <tbody>";
                console.log(data)
                data.forEach(elem => {
                    output_html_ += "<tr id = '"+ elem['id']+"'>";
                    output_html_ += "<td>" + elem['name'] + "</td>";
                    output_html_ += "<td>" + elem['status'] + "</td>";
                });
                output_html_ += "</tbody></table>";
                output_html_ += "<button class='btn' id='outstanding'>Outstanding request<button>";
                $(".content").html(output_html_);
                $("#prev").click(books);
                $(".settings").click(edit_book);
                $(".delete").click(delete_book);
                $("#add").click(add_copies_book);
                $("#sub").click(add_copies_book);
                $("#outstanding").click(outstanding_book);
                feather.replace();
            });
        }else{
            $(".content").html(output_html_);
            $("#prev").click(books);
            $(".settings").click(edit_book);
            $(".delete").click(delete_book);
            $("#add").click(add_copies_book);
            $("#sub").click(add_copies_book);
            feather.replace();
        }
    });
}

function outstanding_book(){
    book_id = $("#id").html();
    console.log(book_id)
    $.post("/api/outstanding", {doc_id:book_id,type:"book"},function (data,status){
        book_info();
    });
}

function add_copies_book() {
    if($(this).attr("id") == "add") {
        $.post("/api/add_copies_of_doc",{id:$("#id").html(), delta_count:1,type:'book'},function (data,status){
            book_info();
        });
    }else {
        $.post("/api/add_copies_of_doc",{id:$("#id").html(), delta_count:-1,type:'book'},function (data,status){
            book_info();
        });
    }
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
    <form>\
    <div class='form-group'>\
    <label for='title'>Title</lable></br>\
    <input type='form-control'id='title' name='title' value='"+book['title']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='authors'>Authors</lable></br>\
    <input type='form-control'id='authors' name='authors' value='"+book['authors']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='description'>Description</lable></br>\
    <input type='form-control'id='description' name='description' value='"+book['description']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='count'>Count</lable></br>\
    <input type='form-control'id='count' name='count' value='"+book['count']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='free_count'>Free count</lable></br>\
    <input type='form-control'id='free_count' name='free_count' value='"+book['free_count']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='price'>Price</lable></br>\
    <input type='form-control'id='price' name='price' value='"+book['price']+"' type='number'>\
    </div>\
    <div class='form-check'>\
    <input type='checkbox' class='form-check-input' id='best_seller'>\
    <label for='best_seller'>Best seller</lable>\
    </div>\
    <div class='form-group'>\
    <label for='keywords'>Keywords</lable></br>\
    <input type='form-control'id='keywords' name='keywords' value='"+book['keywords']+"' type='number'>\
    </div>\
    <button id='save' class='btn'>Save</button><p id='id' hidden>"+book['id']+"</p></form>";
    $(".content").html(output_html);
    $("#save").click(function(event){
        event.preventDefault();
        best_seller = 0;
        if($("#best_seller").is(":checked")){
            best_seller = 1;
        }
        send_data = book = {id:$("#id").html(),title:$("#title").val(),authors:$("#authors").val(),description:$("#description").val(),count:$("#count").val(),free_count:$("#free_count").val(),price:$("#price").val(),best_seller:best_seller,keywords:$("#keywords").val(),type:'book'};
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
    $.post("/api/get_all_doctype",{type:'media'},function(data,status){
        output_html = "<div class='row'>\
        <div class = 'col-5'><h3>Audio visual materials</h3></div>\
        <div class='col-1'><button class='btn btn-sm add'><span data-feather='plus'></span></button></div>\
        </div>\
        <div class='row'><div class='col-md-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
        <div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                    <tr>\
                        <th>Title</th>\
                        <th>Authors</th>\
                        <th>Count</th>\
                        <th>Free count</th>\
                        <th>Price</th>\
                        <th></th>\
                    </tr>\
                </thead>\
                <tbody id='tbody'>";
        console.log(data);
        data.forEach(elem => {
            output_html += "<tr id = '"+ elem['id']+"'>";
            output_html += "<td>" + elem['title'] + "</td>";
            output_html += "<td>" + elem['authors'] + "</td>";
            output_html += "<td>" + elem['count'] + "</td>";
            output_html += "<td>" + elem['free_count'] + "</td>";
            output_html += "<td>" + elem['price'] + "</td>"
            output_html += "<td><button class='btn info'><span data-feather='info'></span></button></td></tr>";
        });
        output_html += "</tbody></table></div>";
        $(".content").html(output_html);
        $(".info").click(av_material_info);
        $(".add").click(edit_av_material);
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
          });
        
        feather.replace();

    });
}

function av_material_info(){
    media_id_ = 0;
    if($("#id").length){
        media_id_ = $("#id").html();
    }else{
        media_id_ = $(this).parent().parent().attr('id');
    }
    console.log(media_id_);
    $.post("/api/get_document",{id:media_id_,type:'media'},function(data,status){
        console.log(data);
        output_html_ = "<p id='id' hidden>"+media_id_+"</p><div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-9'><h3 id='title'>"+data['title']+"</h3></div><div class='col-md-1'><button class='btn btn-sm delete'><span data-feather='trash-2'></span></button></div><div class='col-md-1'><button id = '"+media_id_+"' class='btn btn-sm settings'><span data-feather='settings'></span></div></div>\
        <h5>Authors: </h5><p id='authors'>" + data['authors']+"</p>\
        <div class='row'><div class='col-1'><h5>Count: </h5></div> <div class='col-1'><button id='add' class='btn btn-sm'><span data-feather='plus'></span></button> </div><div class='col-1'><button id='sub' class='btn btn-sm'><span data-feather='minus'></span></button></div></div><p id='count'>"+data['count']+"</p>\
        <h5>Free count: </h5><p id='free_count'>" + data['free_count']+"</p>\
        <h5>Price: </h5><p id='price'>" + data['price']+"</p>\
        <h5>Keywords: </h5><p id='keywords'>" + data['keywords']+"</p>";
        if(data['queue'] != "[]"){ 
            $.post("/api/get_queue_on_document",{doc_id:media_id_,type:'media'},function(data,status){
                output_html_ += "<h5>Queue: </h5><div class='table-responsive'>\
                <table class='table table-striped table-sm'>\
                    <thead>\
                        <tr>\
                            <th>Name</th>\
                            <th>Status</th>\
                        </tr>\
                    </thead>\
                    <tbody>";
                console.log(data)
                data.forEach(elem => {
                    output_html_ += "<tr id = '"+ elem['id']+"'>";
                    output_html_ += "<td>" + elem['name'] + "</td>";
                    output_html_ += "<td>" + elem['status'] + "</td>";
                });
                output_html_ += "</tbody></table>";
                output_html_ += "<button class='btn' id='outstanding'>Clear queue<button>";
                $(".content").html(output_html_);
                $("#prev").click(av_materials);
                $(".settings").click(edit_av_material);
                $(".delete").click(delete_av_material);
                $("#add").click(add_copies_av);
                $("#sub").click(add_copies_av);
                $("#outstanding").click(outstanding_av);
                feather.replace();
            });
        }else{
            $(".content").html(output_html_);
            $("#prev").click(av_materials);
            $(".settings").click(edit_av_material);
            $(".delete").click(delete_av_material);
            $("#add").click(add_copies_av);
            $("#sub").click(add_copies_av);
            feather.replace();
        }
    });
}

function outstanding_av() {
    av_id = $("#id").html();
    $.post("/api/outstanding", {doc_id:av_id,type:"media"},function (data,status){
        av_material_info();
    });
}

function add_copies_av() {
    if($(this).attr("id") == "add") {
        $.post("/api/add_copies_of_doc",{id:$("#id").html(), delta_count:1,type:'media'},function (data,status){
            av_material_info();
        });
    }else {
        $.post("/api/add_copies_of_doc",{id:$("#id").html(), delta_count:-1,type:'media'},function (data,status){
            av_material_info();
        });
    }
}

function edit_av_material(){
    if($(this).attr('id')){
        media = {id:$(this).attr('id'),title:$("#title").html(),authors:$("#authors").html(),description:$("#description").html(),count:$("#count").html(),free_count:$("#free_count").html(),price:$("#price").html(),keywords:$("#keywords").html()};
        new_media = false;
    }else {
        media = {id:'',title:'New AV-Meterial',authors:'',description:'',count:'',free_count:'',price:'',keywords:''};
        new_media = true;
    }
    output_html = "<div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><h3>"+media['title']+"</h3></div></div>\
    <form>\
    <div class='form-group'>\
    <label for='title'>Title</lable></br>\
    <input type='form-control'id='title' name='title' value='"+media['title']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='authors'>Authors</lable></br>\
    <input type='form-control'id='authors' name='authors' value='"+media['authors']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='count'>Count</lable></br>\
    <input type='form-control'id='count' name='count' value='"+media['count']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='free_count'>Free count</lable></br>\
    <input type='form-control'id='free_count' name='free_count' value='"+media['free_count']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='price'>Price</lable></br>\
    <input type='form-control'id='price' name='price' value='"+media['price']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='keywords'>Keywords</lable></br>\
    <input type='form-control'id='keywords' name='keywords' value='"+media['keywords']+"' type='number'>\
    </div>\
    <button id='save' class='btn'>Save</button><p id='id' hidden>"+media['id']+"</p></form>";
    $(".content").html(output_html);
    $("#save").click(function(event){
        event.preventDefault();
        send_data = {id:$("#id").html(),title:$("#title").val(),authors:$("#authors").val(),description:0,count:$("#count").val(),free_count:$("#free_count").val(),price:$("#price").val(),keywords:$("#keywords").val(),best_seller:0,type:'media'};
        console.log(send_data);
        if(new_media){
            $.post("/api/add_document",send_data,function(data,status){
                console.log(data);
                av_materials();
            });
        }else{
            $.post("/api/modify_document",send_data,function(data,status){
                av_material_info();
            });
        }
    });
    if(new_media){
        $("#prev").click(av_materials);
    }else{
        $("#prev").click(av_material_info);
    }

    feather.replace();
}

function delete_av_material(){
    av_material_id_ = $("#id").html();
    $.post("/api/delete_document",{id:av_material_id_,type:'media'},function(data,status){
        av_materials();
    });
}

function articles() {
    $.post("/api/get_all_doctype",{type:'article'},function(data,status){
        output_html = "<div class='row'>\
        <div class = 'col-2'><h3>Articles</h3></div>\
        <div class='col-1'><button class='btn btn-sm add'><span data-feather='plus'></span></button></div>\
        </div>\
        <div class='row'><div class='col-md-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
        <div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                    <tr>\
                        <th>Title</th>\
                        <th>Authors</th>\
                        <th>Journal</th>\
                        <th>Count</th>\
                        <th>Free count</th>\
                        <th></th>\
                    </tr>\
                </thead>\
                <tbody id='tbody'>";
        console.log(data);
        data.forEach(elem => {
            output_html += "<tr id = '"+ elem['id']+"'>";
            output_html += "<td>" + elem['title'] + "</td>";
            output_html += "<td>" + elem['authors'] + "</td>";
            output_html += "<td>" + elem['journal'] + "</td>";
            output_html += "<td>" + elem['count'] + "</td>";
            output_html += "<td>" + elem['free_count'] + "</td>"
            output_html += "<td><button class='btn info'><span data-feather='info'></span></button></td></tr>";
        });
        output_html += "</tbody></table></div>";
        $(".content").html(output_html);
        $(".info").click(article_info);
        $(".add").click(edit_article);
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
          });
        
        feather.replace();

    });
}

function edit_article() {
    if($(this).attr('id')){
        article = {id:$(this).attr('id'),title:$("#title").html(),authors:$("#authors").html(),description:$("#description").html(),count:$("#count").html(),free_count:$("#free_count").html(),price:$("#price").html(),keywords:$("#keywords").html(),journal:$("#journal").html(),issue:$("#issue").html(),editors:$("#editors").html(),date:$("#date").html()};
        new_article = false;
    }else {
        article = {id:'',title:'New article',authors:'',description:'',count:'',free_count:'',price:'',keywords:'',journal:'',issue:'',editors:'',date:''};
        new_article = true;
    }
    output_html = "<div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-10'><h3>"+article['title']+"</h3></div></div>\
    <form>\
    <div class='form-group'>\
    <label for='title'>Title</lable></br>\
    <input type='form-control'id='title' name='title' value='"+article['title']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='authors'>Authors</lable></br>\
    <input type='form-control'id='authors' name='authors' value='"+article['authors']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='journal'>Journal</lable></br>\
    <input type='form-control'id='journal' name='journal' value='"+article['journal']+"' type='text'>\
    </div>\
    <div class='form-group'>\
    <label for='count'>Count</lable></br>\
    <input type='form-control'id='count' name='count' value='"+article['count']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='free_count'>Free count</lable></br>\
    <input type='form-control'id='free_count' name='free_count' value='"+article['free_count']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='price'>Price</lable></br>\
    <input type='form-control'id='price' name='price' value='"+article['price']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='keywords'>Keywords</lable></br>\
    <input type='form-control'id='keywords' name='keywords' value='"+article['keywords']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='issue'>Issue</lable></br>\
    <input type='form-control'id='issue' name='issue' value='"+article['issue']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='editors'>Editors</lable></br>\
    <input type='form-control'id='editors' name='editors' value='"+article['editors']+"' type='number'>\
    </div>\
    <div class='form-group'>\
    <label for='date'>Date of publication</lable></br>\
    <input type='form-control'id='date' name='date' value='"+article['date']+"' type='number'>\
    </div>\
    <button id='save' class='btn'>Save</button><p id='id' hidden>"+article['id']+"</p></form>";
    $(".content").html(output_html);
    $("#save").click(function(event){
        event.preventDefault();
        send_data = {id:$("#id").html(),title:$("#title").val(),authors:$("#authors").val(),description:0,count:$("#count").val(),free_count:$("#free_count").val(),price:$("#price").val(),keywords:$("#keywords").val(),best_seller:0,journal:$("#journal").val(),issue:$("#issue").val(),editors:$("#editors").val(),date:$("#date").val(),type:'article'};
        console.log(send_data);
        if(new_article){
            $.post("/api/add_document",send_data,function(data,status){
                console.log(data);
                articles();
            });
        }else{
            $.post("/api/modify_document",send_data,function(data,status){
                article_info();
            });
        }
    });
    if(new_article){
        $("#prev").click(articles);
    }else{
        $("#prev").click(article_info);
    }

    feather.replace();
}

function article_info() {
    article_id_ = 0;
    if($("#id").length){
        article_id_ = $("#id").html();
    }else{
        article_id_ = $(this).parent().parent().attr('id');
    }
    console.log(article_id_);
    $.post("/api/get_document",{id:article_id_,type:'article'},function(data,status){
        console.log(data);
        output_html_ = "<p id='id' hidden>"+article_id_+"</p><div class='row'><div class='col-md-1'><button id='prev' class='btn btn-sm'><span data-feather='arrow-left'></span></button></div><div class='col-md-9'><h3 id='title'>"+data['title']+"</h3></div><div class='col-md-1'><button class='btn btn-sm delete'><span data-feather='trash-2'></span></button></div><div class='col-md-1'><button id = '"+article_id_+"' class='btn btn-sm settings'><span data-feather='settings'></span></div></div>\
        <h5>Authors: </h5><p id='authors'>" + data['authors']+"</p>\
        <h5>Journal: </h5><p id='journal'>" + data['journal']+"</p>\
        <div class='row'><div class='col-1'><h5>Count: </h5></div> <div class='col-1'><button id='add' class='btn btn-sm'><span data-feather='plus'></span></button> </div><div class='col-1'><button id='sub' class='btn btn-sm'><span data-feather='minus'></span></button></div></div><p id='count'>"+data['count']+"</p>\
        <h5>Free count: </h5><p id='free_count'>" + data['free_count']+"</p>\
        <h5>Price: </h5><p id='price'>" + data['price']+"</p>\
        <h5>Keywords: </h5><p id='keywords'>" + data['keywords']+"</p>\
        <h5>Issue: </h5><p id='issue'>" + data['issue']+"</p>\
        <h5>Editors: </h5><p id='editors'>" + data['editors']+"</p>\
        <h5>Date: </h5><p id='date'>" + data['date']+"</p>";
        if(data['queue'] != "[]"){ 
            $.post("/api/get_queue_on_document",{doc_id:$("#id").html(),type:'article'},function(data,status){
                output_html_ += "<h5>Queue: </h5><div class='table-responsive'>\
                <table class='table table-striped table-sm'>\
                    <thead>\
                        <tr>\
                            <th>Name</th>\
                            <th>Status</th>\
                        </tr>\
                    </thead>\
                    <tbody>";
                console.log(data)
                data.forEach(elem => {
                    output_html_ += "<tr id = '"+ elem['id']+"'>";
                    output_html_ += "<td>" + elem['name'] + "</td>";
                    output_html_ += "<td>" + elem['status'] + "</td>";
                });
                output_html_ += "</tbody></table>";
                output_html_ += "<button class='btn' id='outstanding'>Clear queue<button>";
                $(".content").html(output_html_);
                $("#prev").click(articles);
                $(".settings").click(edit_article);
                $(".delete").click(delete_article);
                $("#add").click(add_copies_article);
                $("#sub").click(add_copies_article);
                $("#outstanding").click(outstanding_article);
                feather.replace();
            });
        }else{
            $(".content").html(output_html_);
            $("#prev").click(articles);
            $(".settings").click(edit_article);
            $(".delete").click(delete_article);
            $("#add").click(add_copies_article);
            $("#sub").click(add_copies_article);
            feather.replace();
        }
    });
}

function outstanding_article(){
    article_id = $("#id").html();
    $.post("/api/outstanding", {doc_id:article_id,type:"article"},function (data,status){
        article_info();
    });
}

function add_copies_article() {
    if($(this).attr("id") == "add") {
        $.post("/api/add_copies_of_doc",{id:$("#id").html(), delta_count:1,type:'article'},function (data,status){
            article_info();
        });
    }else {
        $.post("/api/add_copies_of_doc",{id:$("#id").html(), delta_count:-1,type:'article'},function (data,status){
            article_info();
        });
    }
}

function delete_article(){
    article_id_ = $("#id").html();
    $.post("/api/delete_document",{id:article_id_,type:'article'},function(data,status){
        articles();
    });
}

function orders_event(event) {
    event.preventDefault();
    bar_user = "<div class='row'><div class ='col-10 content'></div><div class='col-2 sidebar-wrapper'><ul class='sidebar-nav'><li><button class='btn btn-sm ' id ='awaiting'>Awaiting orders</button></li>\
    <li><button class='btn btn-sm' id ='active'>Active Orders</button></li>\
    </ul></div></div>";
    $(".main").html(bar_user);
    awaiting_orders();
    $("#awaiting").click(awaiting_orders);
    $("#active").click(active_orders);
}

function awaiting_orders() {
    $.post("/api/get_all_waiting_doc",{},function(data,status){
        output_html = "<div class='row'>\
        <div class = 'col-3'><h3>Awaiting orders</h3></div>\
        </div>\
        <div class='row'><div class='col-md-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
        <div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                    <tr>\
                        <th>User</th>\
                        <th>Title</th>\
                        <th>Authors</th>\
                        <th>Type</th>\
                        <th>Ordering time</th>\
                        <th>Return time</th>\
                        <th>User Get Document</th>\
                    </tr>\
                </thead>\
                <tbody class='tbody'>";
        console.log(data);
        data.forEach(elem => {
            output_html += "<tr id = '"+ elem['id']+"'>";
            output_html += "<td>" + elem['user']['name'] + "</td>";
            output_html += "<td>" + elem['doc']['title'] + "</td>";
            output_html += "<td>" + elem['doc']['authors'] + "</td>";
            output_html += "<td>" + elem['table'] + "</td>";
            output_html += "<td>" + elem['time'] + "</td>";
            output_html += "<td>" + elem['time_out'] + "</td>";
            output_html += "<td><button class='btn btn-sm get'><span data-feather='check'></span></button> \0 <button class='btn btn-sm delete'><span data-feather='trash-2'></span></button></td></tr>";
        });
        output_html += "</tbody></table></div>";
        $(".content").html(output_html);
        $(".get").click(user_get_doc);
        $(".delete").click(delete_order);
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
          });
        
        feather.replace();
    });
}

function user_get_doc(){
    order_id_ = $(this).parent().parent().attr("id");
    $.post("/api/user_get_doc",{order_id:order_id_},function(data,status){});
    $(this).parent().parent().remove();
}

function delete_order(){

}

function active_orders() {
    $.post("/api/get_all_active_orders",{},function(data,status){
        output_html = "<div class='row'>\
        <div class = 'col-3'><h3>Active orders</h3></div>\
        </div>\
        <div class='row'><div class='col-md-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
        <div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                    <tr>\
                        <th>User</th>\
                        <th>Title</th>\
                        <th>Authors</th>\
                        <th>Type</th>\
                        <th>Ordering time</th>\
                        <th>Return time</th>\
                        <th>User Return Document</th>\
                    </tr>\
                </thead>\
                <tbody class='tbody'>";
        console.log(data);
        data.forEach(elem => {
            output_html += "<tr id = '"+ elem['id']+"'>";
            output_html += "<td>" + elem['user']['name'] + "</td>";
            output_html += "<td>" + elem['doc']['title'] + "</td>";
            output_html += "<td>" + elem['doc']['authors'] + "</td>";
            output_html += "<td>" + elem['table'] + "</td>";
            output_html += "<td>" + elem['time'] + "</td>";
            output_html += "<td>" + elem['time_out'] + "</td>";
            output_html += "<td><button class='btn btn-sm return'><span data-feather='check'></span></button></td></tr>";
        });
        output_html += "</tbody></table></div>";
        $(".content").html(output_html);
        $(".return").click(user_return_doc);
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
          });
        
        feather.replace();
    });
}

function user_return_doc() {
    order_id_ = $(this).parent().parent().attr("id");
    $.post("/api/return_doc",{order_id:order_id_},function(data,status){
        alert(data);
    });
    $(this).parent().parent().remove();
}

function history_event(event) {
    event.preventDefault();
    bar_user = "<div class='row'><div class ='col-12 content'></div></div>";
    $(".main").html(bar_user);
    $.post("/api/get_all_returned_doc",{},function(data,status){
        output_html = "<div class='row'>\
        <div class = 'col-4'><h3>History of orders</h3></div>\
        </div>\
        <div class='row'><div class='col-md-12'><input id='search' class='form-control w-100' placeholder='Search' aria-label='Search' type='text'></div></div>\
        <div class='table-responsive'>\
            <table class='table table-striped table-sm'>\
                <thead>\
                    <tr>\
                        <th>User</th>\
                        <th>Title</th>\
                        <th>Authors</th>\
                        <th>Type</th>\
                        <th>Ordering time</th>\
                        <th>Return time</th>\
                    </tr>\
                </thead>\
                <tbody class='tbody'>";
        console.log(data);
        data.forEach(elem => {
            output_html += "<tr id = '"+ elem['id']+"'>";
            output_html += "<td>" + elem['user']['name'] + "</td>";
            output_html += "<td>" + elem['doc']['title'] + "</td>";
            output_html += "<td>" + elem['doc']['authors'] + "</td>";
            output_html += "<td>" + elem['table'] + "</td>";
            output_html += "<td>" + elem['time'] + "</td>";
            output_html += "<td>" + elem['time_out'] + "</td>";
            output_html += "</tr>";
        });
        output_html += "</tbody></table></div>";
        $(".content").html(output_html);
        $("#search").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            $("#tbody tr").filter(function() {
              $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
          });
        
        feather.replace();
    });
}
