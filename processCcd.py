from lsst.meas.base.sfm import SingleFrameMeasurementTask
root.calibrate.initialMeasurement.retarget(SingleFrameMeasurementTask)
#root.calibrate.photocal.doWriteOutput=False
root.calibrate.measurement.retarget(SingleFrameMeasurementTask)
root.measurement.retarget(SingleFrameMeasurementTask)
root.measurement.slots.instFlux = "base_NaiveFlux"
