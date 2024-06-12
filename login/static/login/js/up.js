document.getElementById('select-all').onclick = function() {
    var checkboxes = document.getElementsByName('user_usernames');
    for (var checkbox of checkboxes) {
        checkbox.checked = this.checked;
    }
}