# coding=SJIS

u"""
���C�����W���[�� �e�X�g�p
"""

# �e��ݒ�
import sys 
sys.setrecursionlimit(100000) 
sys.dont_write_bytecode = True
import time

# �J�����g�f�B���N�g���̐ݒ�
import os as os
workdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(workdir) 

# �K�v�ȃ��W���[���̓ǂݍ���
import Utility.Input as Input
from Model.CreateModel import CreateModel

def run():
    u"�v�Z�̎��s���s���A���|�[�g���o�͂���"

    asm = Input.Assumption("files_input\\Assumption.csv")
    cells = Input.Cell.LoadCells("files_input\\Cells.csv")

    file_resultreport = open('files_result\\ResultReport.csv','w')
    file_dumpreport = open('files_result\\DumpReport.csv','w')

    for i in range(0, len(cells)):
        model = CreateModel(cells[i], asm)
        
        # �w�b�_�[�̋L�q
        if i == 0:
            file_resultreport.write(
               "%s,%s,%s\n" % ("Descripton", "No", model.ResultReportHeader()))

        desc = cells[i].get_str("Description")
        file_resultreport.write("%s,%d,%s\n" % (desc, i, model.ResultReportValues()))
        for item in model.DumpReport(): 
            file_dumpreport.write("%s,%d,%s\n" % (desc, i, item))    
        
        print "cell %d finished" % (i)

    file_resultreport.close()
    file_dumpreport.close()


def main():
    u"���C�����\�b�h"
    
    starttime = time.clock()
    run()
    time1 = time.clock()
    print "time: %f" % (time1 - starttime)

main()
