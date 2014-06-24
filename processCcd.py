from lsst.meas.base.sfm import SingleFrameMeasurementTask
root.measurement.retarget(SingleFrameMeasurementTask)
root.calibrate.initialMeasurement.retarget(SingleFrameMeasurementTask)
root.calibrate.initialMeasurement.plugins = ["base_SdssCentroid","skycoord", "base_SdssShape", "base_GaussianFlux", "base_PsfFlux", "base_SincFlux", "base_NaiveFlux", "base_PixelFlags"]
root.calibrate.initialMeasurement.slots.centroid = "base_SdssCentroid"
root.calibrate.initialMeasurement.slots.shape = "base_SdssShape"
root.calibrate.initialMeasurement.slots.psfFlux = "base_PsfFlux"
root.calibrate.initialMeasurement.slots.modelFlux = None
root.calibrate.initialMeasurement.slots.apFlux = None
root.calibrate.initialMeasurement.slots.instFlux = None
root.calibrate.measurement.retarget(SingleFrameMeasurementTask)
root.calibrate.measurement.plugins = ["base_SdssCentroid","skycoord", "base_SdssShape", "base_GaussianFlux", "base_PsfFlux", "base_SincFlux", "base_NaiveFlux", "base_PixelFlags"]
root.calibrate.measurement.slots.centroid = "base_SdssCentroid"
root.calibrate.measurement.slots.shape = "base_SdssShape"
root.calibrate.measurement.slots.psfFlux = "base_PsfFlux"
root.calibrate.measurement.slots.modelFlux = None
root.calibrate.measurement.slots.apFlux = None
root.calibrate.measurement.slots.instFlux = None
 
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.retarget(SingleFrameMeasurementTask)
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.plugins = ["base_SdssCentroid", "base_SdssShape", "base_PsfFlux", "base_NaiveFlux"]
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.centroid = "base_SdssCentroid"
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.shape = "base_SdssShape"
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.psfFlux = "base_PsfFlux"
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.modelFlux = None
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.apFlux = "base_NaiveFlux"
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.instFlux = None
root.calibrate.measurePsf.starSelector["secondMoment"].badFlags = ["base_PixelFlags_flag_edge",
       "base_PixelFlags_flag_interpolatedCenter",
       "base_PixelFlags_flag_saturatedCenter",
       "base_PixelFlags_flag_crCenter",
    ]


root.measurement.plugins = ["base_SdssCentroid","skycoord", "classification",  "base_SdssShape", "base_GaussianFlux", "base_PsfFlux", "base_SincFlux", "base_NaiveFlux", "base_PixelFlags"]
root.measurement.slots.centroid = "base_SdssCentroid"
root.measurement.slots.shape = "base_SdssShape"
root.measurement.slots.psfFlux = "base_PsfFlux"
root.measurement.slots.modelFlux = "base_GaussianFlux"
root.measurement.slots.apFlux = "base_SincFlux"
root.measurement.slots.instFlux = "base_NaiveFlux"
