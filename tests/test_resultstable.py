from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import hobbit.resultstable as rt
import pytest
import shutil
import tempfile
import csv
import os

@pytest.mark.run(order=3)
def test_resultstable_methods():
    """
    Creates a temporary results table, populates it and tests its methods

    """
    tmp_folder = tempfile.mkdtemp(prefix='test_repo')
    restab = rt.ResultsTable(tmp_folder)

    # test set for adding
    run = 1
    for id in range(1, 11):
        hparams = {'num_layers': id}
        restab.set(run_id=(run, id), hparams=hparams, val_loss=id/100)  # create new entries

    # retrieve test_k best models
    test_k = 5
    k_best = restab.get_k_lowest_from_run(k=test_k, run=1)
    for the_id, expected_id in zip(k_best, range(1, test_k)):
        assert the_id == expected_id


    # manually load tmp_folder/results.csv
    with open(os.path.join(tmp_folder, 'results.csv')) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for i, line in enumerate(reader, start=1):
            print(line)
            run_id, hparams, id, run, val_loss = line
            assert int(run) == 1
            assert int(id) == i
            print(hparams)
            assert hparams == '{\'num_layers\': ' + str(i) + '}'
            assert float(val_loss) == i/100.

    # test set for updating
    restab.set(run_id=(1, 2), val_loss=0.9)
    assert restab.get_val_loss((1, 2)) == 0.9
    assert restab.get_k_lowest_from_run(k=1, run=1) == [1]

    shutil.rmtree(tmp_folder)

if __name__ == '__main__':
    pytest.main([__file__])