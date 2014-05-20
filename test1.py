#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2008-2013 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

import math
import sys
import os
from lsst.afw.table import Schema,SchemaMapper,SourceCatalog,SourceTable
from lsst.meas.base.sfm import SingleFramePluginConfig, SingleFramePlugin, SingleFrameMeasurementTask
from lsst.meas.base.base import *
from lsst.meas.base.tests import *
import unittest
import lsst.utils.tests
import numpy

numpy.random.seed(1234)

#   This script compares the output from processCcd0 in mmout0 with
#   the output from processCcd in mmout1
#
#   This is a test of all the Fluxes -- Gaussian, Sinc, Naive, and Psf.  (Ap is reserved for later)
#   The record passes if either the value, error, or flag are the same, are both nan,
#   or in the case of PsfFlux, differ only by less than .1 percent
#
#   Centroid is also included, since they all need Centroid to work.
if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print "Usage: %s visit"%(sys.argv[0],)
        sys.exit(1)
    # The visit comes in as the first argument on the command line.
    visit = sys.argv[1] 
    DATA_FILE = "mmout1/src/v%s-fi/R22/S11.fits"%(visit,)
    DATA_FILE0 = "mmout0/src/v%s-fi/R22/S11.fits"%(visit,)

    # get the data files from previous pipline runs and compare them
    # the slots have to be set up correctly for this comparison to work
    # so check them first
    measCat0 = SourceCatalog.readFits(DATA_FILE0)
    measCat = SourceCatalog.readFits(DATA_FILE)
    assert(measCat.getCentroidDefinition()=="base_SdssCentroid")
    assert(measCat.getPsfFluxDefinition()=="base_PsfFlux")
    assert(measCat.getModelFluxDefinition()=="base_GaussianFlux")
    assert(measCat.getInstFluxDefinition()=="base_NaiveFlux")
    assert(measCat.getApFluxDefinition()=="base_SincFlux")
    assert(measCat0.getCentroidDefinition()=="centroid.sdss")
    assert(measCat0.getPsfFluxDefinition()=="flux.psf")
    assert(measCat0.getModelFluxDefinition()=="flux.gaussian")
    assert(measCat0.getInstFluxDefinition()=="flux.naive")
    assert(measCat0.getApFluxDefinition()=="flux.sinc")
    assert(len(measCat) == len(measCat0))
    records = 0

#---------------------------------------------------------------
    # The Centroid slot should be run first, and has to give consistent results for the
    # rest of the algorithms comparisons to be valid.
    # In some cases, the new centroid algorithm will give Nans.  That is Ok as long as
    # the footprint peak centroid is the same
    for i in range(len(measCat)):
        record = measCat[i]
        record0 = measCat0[i]
        error = record.getCentroidErr()
        error0 = record0.getCentroidErr()
        flag = record.getCentroidFlag()
        flag0 = record0.getCentroidFlag()
        value = record.getCentroid()
        if numpy.isnan(value.getX()):
            value = record.getFootprint().getPeaks()[0].getF()
        value0 = record0.getCentroid()
        label = "Centroid: "
        if not (value==value0):
            print label, record.getCentroid(), record.getId(), value, value0, flag, flag0

#---------------------------------------------------------------
        # Check the PsfFlux in the PsfFlux slot.  Note that the PsfFlux code was rewritten, and does not quite
        # behave the same. However, most of the values are within .1%, which is what this test shows.
        # The new code also 
        value = record.getPsfFlux()
        value0 = record0.getPsfFlux()
        error = record.getPsfFluxErr()
        error0 = record0.getPsfFluxErr()
        flag = record.getPsfFluxFlag()
        flag0 = record0.getPsfFluxFlag()
        label = "PsfFlux: "
        if not (abs((value-value0)/value0)<.001) and not(numpy.isnan(value)) and not record.get("base_PsfFlux_flag_edge"):
            print label, "Values: ", record.getId(), record.getCentroid(), record0.getCentroid(), value, value0
        if (flag0 != flag):
            print label, "Flags: ", record.getId(), record.getCentroid(), record0.getCentroid(), flag, flag0
        if not (abs((error-error0)/error0)<.001) and not(numpy.isnan(error)) and not record.get("base_PsfFlux_flag_edge"):
            print label, "Errors: ", record.getCentroid(), record.getId(), error, error0

#---------------------------------------------------------------
        # Check the NaiveFlux in the InstFlux slot
        value = record.getInstFlux()
        value0 = record0.getInstFlux()
        error = record.getInstFluxErr()
        error0 = record0.getInstFluxErr()
        flag = record.getInstFluxFlag()
        flag0 = record0.getInstFluxFlag()
        error = record.getInstFluxErr()
        error0 = record0.getInstFluxErr()
        label = "NaiveFlux: "
        if not (value==value0) and not(numpy.isnan(value) and numpy.isnan(value0)):
            print label, record.getCentroid(), record.getId(), value, value0
        if (flag0 != flag):
            print label, "Flags: ", record.getCentroid(), record.getId(), flag, flag0
        if not (error==error0) and not(numpy.isnan(error) and numpy.isnan(error0)):
            print label, "Errors: ", record.getCentroid(), record.getId(), error, error0
#---------------------------------------------------------------
        # Check the SincFlux in the ApFlux slot
        value = record.getApFlux()
        value0 = record0.getApFlux()
        error = record.getApFluxErr()
        error0 = record0.getApFluxErr()
        flag = record.getApFluxFlag()
        flag0 = record0.getApFluxFlag()
        error = record.getApFluxErr()
        error0 = record0.getApFluxErr()
        label = "SincFlux: "
        if not (value==value0) and not(numpy.isnan(value) and numpy.isnan(value0)):
            print label, record.getCentroid(), record.getId(), value, value0
        if (flag0 != flag):
            print label, "Flags: ", record.getCentroid(), record.getId(), flag, flag0
        if not (error==error0) and not(numpy.isnan(error) and numpy.isnan(error0)):
            print label, "Errors: ", record.getCentroid(), record.getId(), error, error0

#---------------------------------------------------------------
        # Check the GaussianFlux in the ModelFlux slot
        value = record.getModelFlux()
        value0 = record0.getModelFlux()
        error = record.getModelFluxErr()
        error0 = record0.getModelFluxErr()
        flag = record.getModelFluxFlag()
        flag0 = record0.getModelFluxFlag()
        flag0 = record0.getModelFluxFlag()
        error = record.getModelFluxErr()
        label = "GaussianFlux: "
        if not (value==value0) and not(numpy.isnan(value) and numpy.isnan(value0)):
            print label, record.getCentroid(), record.getId(), value, value0
        if (flag0 != flag):
            print label, "Flags: ", record.getCentroid(), record.getId(), flag, flag0
        if not (error==error0) and not(numpy.isnan(error) and numpy.isnan(error0)):
            print label, "Errors: ", record.getCentroid(), record.getId(), error, error0
        if not (value==value0) and not(numpy.isnan(value) and numpy.isnan(value0)):
            print label, record.getCentroid(), record.getId(), record.getModelFlux(), record0.getModelFlux(), record.getModelFluxFlag(), record0.getModelFluxFlag()
        if (flag0 != flag):
            print label, "Flags: ", record.getCentroid(), record.getId(), record.getModelFlux(), record0.getModelFlux(), record.getModelFluxFlag(), record0.getModelFluxFlag()
        if not (error==error0) and not(numpy.isnan(error) and numpy.isnan(error0)):
            print label, "Errors: ", record.getCentroid(), record.getId(), record.getModelFluxErr(), record0.getModelFluxErr(), record.getModelFluxFlag(), record0.getModelFluxFlag()

        records = records + 1

    print "%d of %d records processed"%(records, len(measCat))
