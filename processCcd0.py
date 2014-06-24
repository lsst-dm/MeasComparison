from lsst.meas.algorithms.measurement import SourceMeasurementTask
root.calibrate.initialMeasurement.retarget(SourceMeasurementTask)
root.calibrate.initialMeasurement.prefix = "initial."
root.calibrate.initialMeasurement.algorithms = ["skycoord", "shape.sdss", "flux.gaussian", "flux.psf", "flux.sinc", "flux.naive", "flags.pixel"]
root.calibrate.initialMeasurement.slots.centroid = "centroid.sdss"
root.calibrate.initialMeasurement.slots.shape = "shape.sdss"
root.calibrate.initialMeasurement.slots.psfFlux = "flux.psf"
root.calibrate.initialMeasurement.slots.modelFlux = None
root.calibrate.initialMeasurement.slots.apFlux = None
root.calibrate.initialMeasurement.slots.instFlux = None
root.calibrate.measurement.retarget(SourceMeasurementTask)
root.calibrate.measurement.prefix = "measurement."
root.calibrate.measurement.algorithms = ["skycoord", "shape.sdss", "flux.gaussian", "flux.psf", "flux.sinc", "flux.naive", "flags.pixel"]
root.calibrate.measurement.slots.centroid = "centroid.sdss"
root.calibrate.measurement.slots.shape = "shape.sdss"
root.calibrate.measurement.slots.psfFlux = "flux.psf"
root.calibrate.measurement.slots.modelFlux = None
root.calibrate.measurement.slots.apFlux = None
root.calibrate.measurement.slots.instFlux = None
 
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.retarget(SourceMeasurementTask)
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.algorithms = ["shape.sdss", "flux.psf", "flux.naive"]
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.centroid = "centroid.sdss"
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.shape = "shape.sdss"
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.psfFlux = "flux.psf"
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.modelFlux = None
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.apFlux = "flux.naive"
root.calibrate.measurePsf.starSelector["secondMoment"].measurement.slots.instFlux = None
root.calibrate.measurePsf.starSelector["secondMoment"].badFlags = ["initial.flags.pixel.edge",
                   "initial.flags.pixel.interpolated.center",
                   "initial.flags.pixel.saturated.center",
                   "initial.flags.pixel.cr.center",
                   ]
root.calibrate.photocal.outputField="classification.photometric"
root.calibrate.photocal.badFlags = ["initial.flags.pixel.edge",
                   "initial.flags.pixel.interpolated.center",
                   "initial.flags.pixel.saturated.center",
                   "initial.flags.pixel.cr.center",
                   ]


root.measurement.retarget(SourceMeasurementTask)
root.measurement.algorithms = ["skycoord", "classification.extendedness", "shape.sdss", "flux.gaussian", "flux.psf", "flux.sinc", "flux.naive", "flags.pixel"]
root.measurement.slots.centroid = "centroid.sdss"
root.measurement.slots.shape = "shape.sdss"
root.measurement.slots.apFlux = "flux.sinc"
root.measurement.slots.modelFlux = "flux.gaussian"
root.measurement.slots.psfFlux = "flux.psf"
root.measurement.slots.instFlux = "flux.naive"
