

var rangeValues =
{
    "1": "$",
    "2": "$$",
    "3": "$$$",
    "4": "$$$$"
};


$(document).ready(function () {

    // on page load, set the text of the label based the value of the range
    $('#rangeText').text(rangeValues[$('#priceInput').val()]);

    // setup an event handler to set the text when the range value is dragged (see event for input) or changed (see event for change)
    $('#priceInput').on('input change', function () {
        $('#rangeText').text(rangeValues[$(this).val()]);
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

