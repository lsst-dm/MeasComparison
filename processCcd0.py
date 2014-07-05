root.calibrate.initialMeasurement.algorithms.names -= ["correctfluxes"]
root.calibrate.photocal.doWriteOutput = True
root.calibrate.measurement.algorithms.names -= ["correctfluxes"]

#root.calibrate.photocal.badFlags = ["flags.pixel.edge",
#                   "flags.pixel.interpolated.center",
#                   "flags.pixel.saturated.center",
#                   "flags.pixel.cr.center",
#                   ]
#
#
root.measurement.algorithms.names -= ["correctfluxes"]
#root.measurement.slots.centroid = "centroid.sdss"
#root.measurement.slots.shape = "shape.sdss"
#root.measurement.slots.apFlux = "flux.sinc"
#root.measurement.slots.modelFlux = "flux.gaussian"
#root.measurement.slots.psfFlux = "flux.psf"
root.measurement.slots.instFlux = "flux.naive"
