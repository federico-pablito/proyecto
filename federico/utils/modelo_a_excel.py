import xlsxwriter
from io import BytesIO


def model_to_excel(model, queryset):
    """
    Converts a Django QuerySet to an Excel file, automatically using model field names as headers.

    :param model: Django model class from which to retrieve field names
    :param queryset: Django QuerySet to be converted
    :return: BytesIO object containing the Excel file
    """
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Retrieve model field names to use as column headers
    column_headers = [field.verbose_name for field in model._meta.fields]

    # Writing the column headers
    for col_num, header in enumerate(column_headers):
        worksheet.write(0, col_num, header)

    # Writing the data rows
    for row_num, obj in enumerate(queryset, start=1):
        for col_num, field in enumerate(model._meta.fields):
            value = getattr(obj, field.name)
            worksheet.write(row_num, col_num, str(value))  # Using str() to handle various data types

    # Close the workbook
    workbook.close()

    # Rewind the buffer
    output.seek(0)

    return output
