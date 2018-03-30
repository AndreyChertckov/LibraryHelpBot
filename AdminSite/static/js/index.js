$(function(){
    $("#users").click(function(event){
        event.preventDefault();
        bar_user = "<div class='bar'><button class='btn btn-sm ' id ='unconfirmed'>Unconfirmed</button>\
        <button class='btn btn-sm' id ='patrons'>Patrons</button>\
        <button class='btn btn-sm' id ='faculty'>Faculty</button>\
        <button class='btn btn-sm' id ='visprofessors'>Visiting Professors</button></div>";
        
        $(".main").html(bar_user);

        $("#unconfirmed").click(function(){
            $.post("/api/get_all_unconfirmed", {}, function(data, status){
                output_html = "<div class='table-responsive'>\
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
                output_html = output_html.concat("</tbody></table></div>");
                $(".main").html(bar_user.concat(output_html));
                feather.replace();
                $(".accept").click(function(){
                    user_id_ = $(this).parent().parent().attr("id");
                    $.post("/api/confirm_user",{user_id:user_id_},function(data,status){
                    });
                    $(this).parent().parent().remove();
                });
            });
        });
    });
    
})