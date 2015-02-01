var PT = {
    // dict of global URLs populated by the server.
    urls: {},
    enrollInTour: function(tourSlug) {
        /* Enroll a user in a tour */
        var postData = {
            slug: tourSlug
        };
        $.post(PT.urls.yourTours, postData, function(data) {
            console.log(data);
        });
    }
}

$(document).on('click', '.enroll-in-tour', function(e) {
    /* User want's to enroll in a course */
    e.stopPropagation()
    var tourSlug = $(this).data('slug');
    PT.enrollInTour(tourSlug);
})