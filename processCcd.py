from lsst.meas.base.sfm import SingleFrameMeasurementTask
root.calibrate.initialMeasurement.retarget(SingleFrameMeasurementTask)
#root.calibrate.photocal.doWriteOutput=False
root.calibrate.measurement.retarget(SingleFrameMeasurementTask)
root.measurement.retarget(SingleFrameMeasurementTask)
plugs = root.measurement.plugins
root.measurement.slots.instFlux = "base_NaiveFlux"
root.measurement.slots.centroid = "base_SdssCentroid"
