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
#from lsst.meas.base.base import *
from lsst.meas.base.tests import *
from lsst.afw.geom import Point2D
import unittest
import lsst.utils.tests
import numpy

numpy.random.seed(1234)

def xcompareValues(val1, val2, tol):
    if numpy.isnan(val1) and numpy.isnan(val2): return True
    if abs(val1-val2)/(val1+val2) > 2.0*tol: return False
    return True

def compareValues(val1, val2, tol):
    if numpy.isnan(val1) and numpy.isnan(val2): return True
    if (val1+val2) == 0:
        if not val1 == 0:
            return abs((val1-val2)/val1) < tol
        return False 
    return abs((val1-val2)/(val1+val2)) < 0.5*tol

def comparePoints(point1, point2, tol):
    if not compareValues(point1.getX(), point2.getX(), tol): return False
    return compareValues(point1.getY(), point2.getY(), tol)

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
        for fluxer in ("Sinc", "Gaussian", "Naive", "Psf", "PeakLikelihood"):
            fluxer0 = fluxer[0].lower() + fluxer[1:]
            value = record.get("base_" + fluxer + "Flux_flux")
            value0 = record0.get("flux." + fluxer0)
            error = record.get("base_" + fluxer + "Flux_fluxSigma")
            error0 = record0.get("flux." + fluxer0 + ".err")
            edgeFlag = None
            try:
                edgeKey =  measCat.getSchema().find("base_" + fluxer + "Flux_flag_edge")
                edgeFlag = record.get(edgeKey.key)
            except:
                pass
            flag = record.get("base_" + fluxer + "Flux_flag")
            flag0 = record0.get("flux." + fluxer0 + ".flags")
            
            if not compareValues(value,value0,.001):
                print fluxer + "Flux values ", record.getId(), record.getCentroid(), value, value0, flag, flag0, edgeFlag
            if not compareValues(error, error0,.001):
                print fluxer + "Flux errors ", record.getId(), record.getCentroid(), error, error0, flag, flag0, edgeFlag
            if not flag == flag0:
                print fluxer + "Flux values ", record.getId(), value, value0, flag, flag0

        records = records + 1

    print "%d of %d records processed"%(records, len(measCat))
