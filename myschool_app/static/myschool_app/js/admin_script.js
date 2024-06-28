// search js scripts


$(document).ready(function () {
    $('#searchBtn').click(function () {
        var searchById = $('#searchById').val();
        var searchByName = $('#searchByName').val();
        var searchByPhone = $('#searchByPhone').val();
        var url = new URL(window.location.href);
        url.searchParams.set('searchById', searchById);
        url.searchParams.set('searchByName', searchByName);
        url.searchParams.set('searchByPhone', searchByPhone);
        window.location.href = url.href;

        // Send search query to backend using AJAX
        $.ajax({
            url: '/search/',
            type: 'GET',
            data: {
                searchById: searchById,
                searchByName: searchByName,
                searchByPhone: searchByPhone
            },
            success: function (response) {
                // Handle the response from the backend
                console.log(response);
                // Update the table or display search results
            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
                // Handle errors if any
            }
        });

        // Select/Deselect All Checkboxes
        $('#selectAll').click(function() {
            $('input[type="checkbox"]').prop('checked', this.checked);
        });

        // Bulk Delete
        $('#bulkDeleteBtn').click(function () {
            var selected = [];
            $('input.student-checkbox:checked').each(function () {
                selected.push($(this).val());
            });
            if (selected.length > 0) {
                if (confirm('Are you sure you want to delete the selected students?')) {
                    $.ajax({
                        url: "{% url 'bulk_delete_students' %}",
                        method: "POST",
                        data: {
                            'ids': selected,
                            'csrfmiddlewaretoken': '{{ csrf_token }}'
                        },
                        success: function (response) {
                            window.location.reload();
                        }
                    });
                }
            } else {
                alert('No students selected.');
            }
        });
    });

});

