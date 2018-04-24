

var rangeValues =
{
    "1": "$",
    "2": "$$",
    "3": "$$$",
    "4": "$$$$"
};

var distancerangeValues =
{
    ".5": "$",
    "1": "$$",
    "1.5": "$$$",
    "4": "$$$$"
};


function myFunction() {
  /* Get the text field */
  var copyText = document.getElementById("myInput");
  /* Select the text field */
  copyText.select();
  /* Copy the text inside the text field */
  document.execCommand("Copy");
  /* Alert the copied text */
  alert('Link copied. ' + copyText.value + '\n\nNow you can paste and share with your friends!');
};

var copy = function(elementId) {

    var input = document.getElementById(elementId);
    var isiOSDevice = navigator.userAgent.match(/ipad|iphone/i);

    if (isiOSDevice) {
      
        var editable = input.contentEditable;
        var readOnly = input.readOnly;

        input.contentEditable = true;
        input.readOnly = false;

        var range = document.createRange();
        range.selectNodeContents(input);

        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);

        input.setSelectionRange(0, 999999);
        input.contentEditable = editable;
        input.readOnly = readOnly;

    } else {
        input.select();
    }

    document.execCommand('copy');
}


$(document).ready(function () {

    // on page load, set the text of the label based the value of the range
    $('#pricerangeText').text(rangeValues[$('#priceInput').val()]);

    // setup an event handler to set the text when the range value is dragged (see event for input) or changed (see event for change)
    $('#priceInput').on('input change', function () {
        $('#pricerangeText').text(rangeValues[$(this).val()]);
    });

});



$(document).ready(function () {

    // on page load, set the text of the label based the value of the range
    $('#distancerangeText').text([$('#rangeInput').val()]);

    // setup an event handler to set the text when the range value is dragged (see event for input) or changed (see event for change)
    $('#rangeInput').on('input change', function () {
        $('#distancerangeText').text([$(this).val()]);
    });

});

var distancerangevalues =
{
    "804": ".5mi",
    "1608": "1mi",
    "3216": "2mi",
    "8040": "5mi",
    "16080": "10mi"
};

$(document).ready(function () {
	var selectedVals = [];
    $('.ui-selected').each(function(k,v) {
        selectedVals.push($(v).text());
    });
    getSelected();
    $('#select-result').val(selectedVals);
    // on page load, set the text of the label based the value of the range
    $('#distancerangeText').text(distancerangevalues[$('#rangeInput').val()]);

    // setup an event handler to set the text when the range value is dragged (see event for input) or changed (see event for change)
    $('#rangeInput').on('input change', function () {
        $('#distancerangeText').text(distancerangevalues[$(this).val()]);
    });

});


var _selectRange = false, _deselectQueue = [];
$(function() {
    $( "#selectable" ).selectable({
        selecting: function (event, ui) {
            if (event.detail == 0) {
                _selectRange = true;
                return true;
            }
            if ($(ui.selecting).hasClass('ui-selected')) {
                _deselectQueue.push(ui.selecting);
            }
        },
        unselecting: function (event, ui) {
            $(ui.unselecting).addClass('ui-selected');
        },
        stop: function () {
            if (!_selectRange) {
                $.each(_deselectQueue, function (ix, de) {
                    $(de)
                        .removeClass('ui-selecting')
                        .removeClass('ui-selected');
                });
            }
            _selectRange = false;
            _deselectQueue = [];
        }
    });
});

function getSelected() {
    var selectedVals = [];
    $('.ui-selected').each(function(k,v) {
        selectedVals.push($(v).text());
    });
}

$('#selectable').click(function() {
    var selectedVals = [];
    $('.ui-selected').each(function(k,v) {
        selectedVals.push($(v).text());
    });
    getSelected();
    $('#cuisine').val(selectedVals);
    console.log(selectedVals);
});


$(document).ready(function RowHider () {

  var results_count = parseInt(document.getElementById("results_count").innerHTML);
  var row_count = results_count+3;
  console.log(results_count);
  console.log(row_count);
    $("tr:gt(" + row_count + ")").hide();

});
