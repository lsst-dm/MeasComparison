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

#  Simple Python routine to compare the meas_algorithm and meas_base misc algorithms
#  Which are pixelflags, classification, skycoord

if __name__ == "__main__":

    if not len(sys.argv) == 2:
        print "Usage: %s visit"%(sys.argv[0],)
        sys.exit(1)
    visit = sys.argv[1] 
    DATA_FILE = "mmout1/src/v%s-fi/R22/S11.fits"%(visit,)
    DATA_FILE0 = "mmout0/src/v%s-fi/R22/S11.fits"%(visit,)

#  Read a catalog for the old (meas_algorithm) and new (meas_base) algorithms
#  These are the result of a complete run of processCcd with default configurations of measurement.py
#  and sfm.py.  "0" means the old meas_algorithm algorithms.  Only the measurement task is different.
#  The pipeline preparatory to measurement should be all the same for both catalogs.   

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
    assert(len(measCat) == len(measCat0))
    for i in range(len(measCat)):
        record = measCat[i]
        record0 = measCat0[i]
 
        # Check the Centroids, but only if at least one of the flags is false.  
        # The centroids behave differently on error for the old and new algorithms 
        error = record.getCentroidErr()
        error0 = record0.getCentroidErr()
        flag = record.getCentroidFlag()
        flag0 = record0.getCentroidFlag()
        value = record.getCentroid()
        value0 = record0.getCentroid()
        label = "Centroid: "
        if not (value==value0) and not(flag and flag0):
            print label, record.getCentroid(), record.getId(), record.getCentroid(), record0.getCentroid(), record.getCentroidFlag(), record0.getCentroidFlag()

#---------------------------------------------------------------
        # test classification
        value = record.get("classification_extendedness")
        value0= record0.get("classification.extendedness")
        label = "Classification: "
        if not (value == value0) and  not(numpy.isnan(value) and numpy.isnan(value0)) and not record.get("base_PsfFlux_flag_edge"):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
            print "new model, psf: ", record.getModelFlux(), record.getPsfFlux(), record.getModelFluxFlag(), record.getPsfFluxFlag()
            print "old model, psf: ", record0.getModelFlux(), record0.getPsfFlux(), record0.getModelFluxFlag(), record0.getPsfFluxFlag()

        # test PixelFlags:  compare them all individually
#---------------------------------------------------------------
        value = record.get("base_PixelFlags_flag_edge")
        value0 = record0.get("flags.pixel.edge")
        label = "PixelFlagsEdge: "
        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
#---------------------------------------------------------------
        value = record.get("base_PixelFlags_flag_interpolated")
        value0 = record0.get("flags.pixel.interpolated.any")
        label = "PixelFlagsInterpolated: "
        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
#---------------------------------------------------------------
        value = record.get("base_PixelFlags_flag_interpolatedCenter")
        value0 = record0.get("flags.pixel.interpolated.center")
        label = "PixelFlagsInterpolatedCenter: "
        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0

            footprint = record.getFootprint()
            footprint0 = record0.getFootprint()
            if (footprint != footprint0):
                if footprint.getCentroid() != footprint0.getCentroid():
                    print record.getFootprint().getCentroid(), record0.getFootprint().getCentroid()
                spans = record.getFootprint().getSpans()
                spans0 = record0.getFootprint().getSpans()
                for i in range(len(spans)):
                    span = spans[i]
                    span0 = spans0[i]
                    if span != span0:
                        print span
                        print span0

#---------------------------------------------------------------
        value = record.get("base_PixelFlags_flag_saturated")
        value0 = record0.get("flags.pixel.saturated.any")
        label = "PixelFlagSaturated: "
        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
#---------------------------------------------------------------
        value = record.get("base_PixelFlags_flag_saturatedCenter")
        value0 = record0.get("flags.pixel.saturated.center")
        label = "PixelFlagSaturatedCenter: "
        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
#---------------------------------------------------------------
        value = record.get("base_PixelFlags_flag_cr")
        value0 = record0.get("flags.pixel.cr.any")
        label = "PixelFlagsCr: "
        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
#---------------------------------------------------------------
        value = record.get("base_PixelFlags_flag_crCenter")
        value0 = record0.get("flags.pixel.cr.center")
        label = "PixelFlagsCrCenter: "
        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
#---------------------------------------------------------------
        value = record.get("base_PixelFlags_flag_bad")
        value0 = record0.get("flags.pixel.bad")
        label = "PixelFlagBad: "
        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0

        if not (value == value0) and  not(numpy.isnan(value)):
            print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
    
#---------------------------------------------------------------
        # test skycoord:  note that these values should never be nan since centroid is never nan
        label = "skycoord: "
        value = record.getCoord()
        value0 = record0.getCoord()
        if not (value == value0):
            if not numpy.isnan(record.getCentroid().getX()) or not numpy.isnan(value.getRa().asDegrees()):
                print label, "Values differ: ", record.getCentroid(), record.getId(), value, value0
