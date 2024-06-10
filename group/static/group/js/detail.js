
var input;
var users = [];
var usersDiv;

$(document).ready(function() {
    //list of all the groups name
    input = document.getElementById('userSearch');
    usersDiv = document.getElementById('users');
    for (var i = 0; i < usersDiv.children.length; i++) {
        //only get the group name
        users.push({
            "name":usersDiv.children[i].getElementsByClassName('userName')[0].innerHTML,
            "html":usersDiv.children[i]
        });
    }

    //search for a group
    input.addEventListener('keyup', searchGroup);
});

function searchGroup() {
    var filter = input.value.toUpperCase();
    for (var i = 0; i < users.length; i++) {
        if (users[i].name.toUpperCase().indexOf(filter) > -1) {
            users[i].html.hidden = false;
        } else {
            users[i].html.hidden = true;
        }
    }
}