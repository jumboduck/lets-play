// Every reaction button
$(document).on("click", ".reaction-link", function () {
    // Determine which image is being targeted for the request via the id
    let loop = getNumberFromId($(this).attr("id"));
    // Determine which reaction is used via the id
    let reaction = getReactionFromId($(this).attr("id"));
    // Get the image id in the db
    let imageId = $(this).attr("image-id");
    // Construct the id of the element that will be updated
    let displayElement = `#${reaction}-num-${loop}`;
    // Construct the url for the ajax request
    let url = `/update_reaction/${imageId}/${reaction}`;
    // Send information to the server
    sendReaction(url, $(this), displayElement);
});

// Get the number at the end of id, helps us determine which image is targeted
function getNumberFromId(id) {
    return id.match(/\d+/g)[0];
}

// Get the reaction used from the id attribute
function getReactionFromId(id) {
    return id.match(/[a-zA-Z]+/g)[0];
}

// Update fields in db, return new value for reactions and change the class of the button
function sendReaction(url, button, feedbackEl) {
    $.ajax({
        type: "POST",
        url: url,
    }).done((data) => {
        $(feedbackEl).text(data.new_value);
        button.toggleClass("selected");
    });
}
