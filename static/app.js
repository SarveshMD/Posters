document.querySelector("#search").addEventListener("submit", function (e) {
    let checked = document.querySelector("#tv_show").checked;
    if (checked) {
        this.action = "/results/tv";
    } else {
        this.action = "/results/film";
    }
})