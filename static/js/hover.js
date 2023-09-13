function overDash(){
    let image = document.getElementById('image_dash');
    image.setAttribute("src", "src/dashboard.png")
}
function outDash(){
    let image = document.getElementById('image_dash');
    image.setAttribute("src", "src/dashboard_gray.png")
}
function overWebcam() {
    let image = document.getElementById('image_web');
    image.setAttribute("src", "{% static 'src/go.png' %}")
}
function outWebcam(){
    let image = document.getElementById('image_web');
    image.setAttribute("src", "{% static 'src/go_gray.png' %}")
}
function overleave() {
    let image = document.getElementById('image_leave');
    image.setAttribute("src", "{% static 'src/out.png' %}")
}
function outleave(){
    let image = document.getElementById('image_leave');
    image.setAttribute("src", "{% static 'src/out_gray.png' %}")
}
function overStat() {
    let image = document.getElementById('image_stat');
    image.setAttribute("src", "src/statistics.png")
}
function outStat(){
    let image = document.getElementById('image_stat');
    image.setAttribute("src", "src/statistics_gray.png")
}
function overWork() {
    let image = document.getElementById('image_work');
    image.setAttribute("src", "src/work-area.png")
}
function outWork(){
    let image = document.getElementById('image_work');
    image.setAttribute("src", "src/work-area_gray.png")
}