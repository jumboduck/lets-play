$("document").ready(function () {
    // When the mouse hovers over a nav link it applies the class to scale the link
    // and when it leaves, it removes class
});

// Update fields in db
function sendData(fieldData, url, feedbackEl) {
    $.ajax({
        data: fieldData,
        type: "POST",
        url: url,
    }).done((data) => {
        $(feedbackEl).text(data.new_value);
    });
}
