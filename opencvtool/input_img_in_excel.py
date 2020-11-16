from opencvtool import CutMainObject
import xlsxwriter


test = CutMainObject(
    '../opencvtool/images/images_ATHLETIC TAB ST WHITE.png', '../opencvtool/out/')
img_file=test.Save()



# 插入图片到表格
book = xlsxwriter.Workbook('pict.xlsx')

sheet = book.add_worksheet('demo')

sheet.insert_image('D4',img_file)

book.close()