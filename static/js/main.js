$("document").ready(function(){

    // When the mouse hovers over a nav link it applies the class to scale the link
    // and when it leaves, it removes class

    $(".menu-link").on("mouseenter", event => {
        $(event.currentTarget).addClass("menu-link-zoom");
    }).on("mouseleave", event => {
        $(event.currentTarget).removeClass("menu-link-zoom");
    })
})