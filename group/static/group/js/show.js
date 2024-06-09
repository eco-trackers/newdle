
var input;
var groups = [];
var groupDiv;

$(document).ready(function() {
    //list of all the groups name
    input = document.getElementById('groupSearch');
    groupsDiv = document.getElementById('groups');
    for (var i = 0; i < groupsDiv.children.length; i++) {
        //only get the group name
        groups.push({
            "name":groupsDiv.children[i].getElementsByClassName('groupName')[0].innerHTML,
            "html":groupsDiv.children[i]
        });
    }

    //search for a group
    input.addEventListener('keyup', searchGroup);
});

function searchGroup() {
    var filter = input.value.toUpperCase();
    for (var i = 0; i < groups.length; i++) {
        if (groups[i].name.toUpperCase().indexOf(filter) > -1) {
            groups[i].html.hidden = false;
        } else {
            groups[i].html.hidden = true;
        }
    }
}