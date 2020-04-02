$("#threadStartButton").click(function() {
    $.get("/output/", function(data) {
        $("#threadStartOutput").html(data);
    }, "html");
});

console.log("Success")