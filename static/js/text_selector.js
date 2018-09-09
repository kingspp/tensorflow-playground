/**
 * Created by prathyushsp on 07/07/16.
 */
var parentContainerClass = ".child_card";

$(document).ready(function () {
    loadTextSelector(parentContainerClass);
});

function loadTextSelector(containerClass) {
    if (!window.CurrentSelection) {
        CurrentSelection = {}
    }
    CurrentSelection.Selector = {};
    //get the current selection
    CurrentSelection.Selector.getSelected = function () {
        var sel = '';
        if (window.getSelection) {
            sel = window.getSelection()
        }
        else if (document.getSelection) {
            sel = document.getSelection()
        }
        else if (document.selection) {
            sel = document.selection.createRange()
        }
        return sel
    };
    //function to be called on mouseup
    CurrentSelection.Selector.mouseup = function () {
        var st = CurrentSelection.Selector.getSelected();
        if (document.selection && !window.getSelection) {
            var range = st;
            range.pasteHTML("<span class='selectedText'>" + range.htmlText + "</span>");
        }
        else {
            var range = st.getRangeAt(0);
            var newNode = document.createElement("span");
            newNode.setAttribute("class", "selectedText");
            range.surroundContents(newNode);
            var getTitle = newNode.innerHTML;
            newNode.setAttribute("title", getTitle);
            var _id = range.startContainer.id.split("#")[1];
            if (getTitle && getTitle != "" && getTitle != '\n') {
                if (getTitle.search("<span")) {
                    getTitle = getTitle.replace(/<\/?span[^>]*>/ig, "");
                }
                getVariableEndPoint = endPoint + "/get-variable/" + _id + '/' + getTitle;
                HTTPUtil.GET(getVariableEndPoint,
                    function (res, err) {
                        if (res === null) {
                            console.log("Exception while getting the data from the server");
                        } else {
                            if (res.status == 500) {
                                jsonData = "Server Error!!"
                            }
                            else if (res.status == 404) {
                                jsonData = "No such var"
                            }
                            else {
                                jsonData = res;
                                var popDiv = document.createElement('span');
                                popDiv.setAttribute('class', 'popDiv');
                                popDiv.innerHTML = jsonData;

                                if (newNode.innerHTML.length > 0) {
                                    newNode.appendChild(popDiv);
                                }
                                //Remove Selection: To avoid extra text selection in IE
                                if (window.getSelection) {
                                    window.getSelection().removeAllRanges();
                                }
                                else if (document.selection) {
                                    document.selection.empty();
                                }
                            }
                        }
                    });
            }
        }
    };


    $(function () {
        $(containerClass).on('mouseup', function () {
            $('span.selectedText').contents().unwrap();
            $(this).find('span.popDiv').remove();
        });
        $(containerClass).bind("mouseup", CurrentSelection.Selector.mouseup);
    });

}
