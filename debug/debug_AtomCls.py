
if __name__ == "__main__":

    import sys
    sys.path.append("..")

    from src.Structure import AtomCls
    file = "../atom/config/C_III.Level"
    file_Aji = "../atom/C_III/Einstein_A/Nist.Aji"
    atom = AtomCls.Atom(file, _file_Aji=file_Aji)



    #--- assert that the index - configuration search method works well
    line_index = 2

    line_ctj = atom.line_index_to_line_ctj(line_index)
    line_idx = atom.line_ctj_to_line_idx(line_ctj)
    line_index2 = atom.line_idx_to_line_index(line_idx)

    line_idx = atom.line_index_to_line_idx(line_index)
    line_ctj = atom.line_idx_to_line_ctj(line_idx)
    line_index3 = atom.line_ctj_to_line_index(line_ctj)

    assert line_index == line_index2 == line_index3
