$(function(){
    $("#users").click(function(event){
        event.preventDefault();
        bar_user = "<div bar><button class='btn btn-sm btn-outline-secondary' id ='unconfirmed'>Unconfirmed</button>\
        <button class='btn btn-sm btn-outline-secondary' id ='patrons'>Patrons</button>\
        <button class='btn btn-sm btn-outline-secondary' id ='faculty'>Faculty</button>\
        <button class='btn btn-sm btn-outline-secondary' id ='visprofessors'>Visiting Professors</button>";
        
        $(".main").html(bar_user);

        $("#unconfirmed").click(function(){
            $.post("/api/get_all_unconfirmed", {}, function(data, status){
                alert(data);
            });
        });
    });
    
})