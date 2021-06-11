console.log("test");

window.addEventListener("load" , function (){
    $(".previous_button").on("click",function(){ scroll(this,false); });
    $(".next_button").on("click",    function(){ scroll(this,true); });

});
function scroll(elem,next){
    console.log(elem);
    console.log(next);
    let target  = $(elem).siblings(".preview_data_area");
    let width   = target.outerWidth();

    if (next){
        target.animate({ scrollLeft:"+=" + String(width) } , 300);
    }
    else{
        target.animate({ scrollLeft:"-=" + String(width) } , 300);
    }
}
