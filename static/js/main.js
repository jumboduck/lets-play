$(document).on("click", ".reaction-link", function () {
    let loop = getNumberFromId($(this).attr("id"));
    let reaction = getReactionFromId($(this).attr("id"));
    let imageId = $(this).attr("image-id");
    let displayElement = `#${reaction}-num-${loop}`;
    let url = `/update_reaction/${imageId}/${reaction}`;
    sendReaction(url, displayElement);
});

// Get the number at the end of id, helps us determine which image is targeted
function getNumberFromId(id) {
    return id.match(/\d+/g)[0];
}

// Get the reaction used from the id attribute
function getReactionFromId(id) {
    return id.match(/[a-zA-Z]+/g)[0];
}

// Update fields in db
function sendReaction(url, feedbackEl) {
    $.ajax({
        type: "POST",
        url: url,
    }).done((data) => {
        $(feedbackEl).text(data.new_value);
    });
}
