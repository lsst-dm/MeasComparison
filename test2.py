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
import os
import sys
from lsst.afw.table import Schema,SchemaMapper,SourceCatalog,SourceTable
from lsst.meas.base.sfm import SingleFramePluginConfig, SingleFramePlugin, SingleFrameMeasurementTask
from lsst.meas.base.base import *
from lsst.meas.base.tests import *
import unittest
import lsst.utils.tests
import numpy

numpy.random.seed(1234)

#  This is a comparison test for SdssShape.  It also does SdssCentroid, since the centroid
#  value is used by the Shape algorithm.  Only the values which are supported in the version 0
#  algorithms can be tested (e.g., not xy4 or flux)

def compareArrays(array1, array2, relDiff):
    if not array1.shape[0] == array2.shape[0] or not array1.shape[1] == array2.shape[1]:
         return False
    for i in range(array1.shape[0]):
        for j in range(array1.shape[1]):
            val1 = array1[i][j]
            val2 = array2[i][j]
            if numpy.isnan(val1) and numpy.isnan(val2):
                continue
            if numpy.isnan(val1) or numpy.isnan(val2):
                return False
            if abs(val1 == val2): continue
            if abs(2.0*(val1-val2)/(val1+val2)) < relDiff: continue
            return False
    return True

if __name__ == "__main__":
   
    if not len(sys.argv) == 2:
        print "Usage: %s visit"%(sys.argv[0],)
        sys.exit(1)
    visit = sys.argv[1] 
    DATA_FILE = "mmout1/src/v%s-fi/R22/S11.fits"%(visit,)
    DATA_FILE0 = "mmout0/src/v%s-fi/R22/S11.fits"%(visit,)
    sdssflagcount = 0

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
        value0 = record0.getCentroid()
        label = "Centroid: "
        if not (value==value0) and not(flag and flag0):
            print label, record.getCentroid(), record.getId(), value, value0, flag, flag0

#---------------------------------------------------------------
        #  Now check the Shape (SdssShape)
        value = record.getShape()
        value0 = record0.getShape()
        error = record.getShapeErr()
        flag = record.getShapeFlag()
        error0 = record0.getShapeErr()
        flag0 = record0.getShapeFlag()
        flagExt = record.get("base_SdssShape_flag_unweightedBad") or record.get("base_SdssShape_flag_unweighted") \
            or record.get("base_SdssShape_flag_maxIter") or record.get("base_SdssShape_flag_shift")
        flagExt0 = record0.get("shape.sdss.flags.unweightedbad") or record0.get("shape.sdss.flags.unweighted") \
            or record0.get("shape.sdss.flags.maxiter") or record0.get("shape.sdss.flags.shift")
        label = "Shape: "

        #   The old algorithms sets the Shape and errors even if the flag is set, whereas the new algorithm
        #   can't do that because the results are lost when the error is thrown
        if not (value==value0):
            # if both flags are set, count this as a match, but print the number of these
            if flag and flag0:
                sdssflagcount = sdssflagcount+1
            # it's really a match if both are Nan
            elif not (numpy.isnan(value.getIxx()) and numpy.isnan(value0.getIxx())):
                print label, " Values: ", record.getId(), value, value0
        #   Errors must be withing .1% unless the general flag is set
        if not compareArrays(error,error0, .001) and not (flag and flag0):
            print label, " Errors: ", record.getId(), record.getCentroid()
        if not (flag == flag0):
                print label, " Flags: ", record.getId(), flag,value,flag0,value0 
                print record.getShapeFlag(), record.get("base_SdssShape_flag_unweightedBad"), \
                    record.get("base_SdssShape_flag_unweighted"), record.get("base_SdssShape_flag_maxIter"), \
                    record.get("base_SdssShape_flag_shift")
                print record0.getShapeFlag(), record0.get("shape.sdss.flags.unweightedbad"), \
                    record0.get("shape.sdss.flags.unweighted"), record0.get("shape.sdss.flags.maxiter"), \
                    record0.get("shape.sdss.flags.shift")

        # We can also check the centroid.  This is the only additional value surfaced by the old algorithm
        value0 = record0.get("shape.sdss.centroid")
        value = lsst.afw.geom.geomLib.Point2D(record.get("base_SdssShape_x"), record.get("base_SdssShape_y"))
        label = "Shape Centroid: "
        if not (value==value0) and not (flag0 and flag):
            print label, " Values: ", record.getId(), value, value0
        records = records + 1

    print "%d of %d records processed"%(records, len(measCat))
    print "Sdss flags set on %d records"%(sdssflagcount,)
