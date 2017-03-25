# -*- coding: utf-8 -*-

from qgis.core import Qgis, QgsUnitTypes

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.parameters import (ParameterVector,
                                        ParameterRaster,
                                        ParameterNumber,
                                        ParameterBoolean,
                                        ParameterSelection,
                                        ParameterTableField)
from processing.core.outputs import OutputDirectory
from processing.tools import dataobjects

from viewshedanalysis import visibility


class ViewshedVariable(GeoAlgorithm):

    DEM = 'DEM'
    OBSERVER_POINTS = 'OBSERVER_POINTS'
    OBSERVER_ID = 'OBSERVER_ID'
    OBSERVER_HEIGHT = 'OBSERVER_HEIGHT'
    TARGET_HEIGHT = 'TARGET_HEIGHT'
    SEARCH_RADIUS = 'SEARCH_RADIUS'
    USE_CURVATURE = 'USE_CURVATURE'
    REFRACTION = 'REFRACTION'
    PRECISION = 'PRECISION'
    ANALYSIS_TYPE = 'ANALYSIS_TYPE'
    CUMULATIVE = 'CUMULATIVE'
    OUTPUT = 'OUTPUT'

    PRECISIONS = ['Coarse', 'Normal', 'Fine']
    TYPES = ['Binary viewshed', 'Invisibility depth', 'Horizon', 'Horizon full']

    def defineCharacteristics(self):
        self.name = 'Viewshed (variable)'
        self.group = 'Visibility analysis'

        self.addParameter(ParameterRaster(
            self.DEM,
            self.tr('Digital elevation model')))
        self.addParameter(ParameterVector(
            self.OBSERVER_POINTS,
            self.tr('Observer location(s)'),
            dataobjects.TYPE_VECTOR_POINT))
        self.addParameter(ParameterTableField(
            self.OBSERVER_ID,
            self.tr('Observer ids (leave unchanged to use feature ids)'),
            self.OBSERVER_POINTS,
            optional=True))
        self.addParameter(ParameterTableField(
            self.OBSERVER_HEIGHT,
            self.tr('Observer height, meters'),
            self.OBSERVER_POINTS)
        self.addParameter(ParameterTableField(
            self.TARGET_HEIGHT,
            self.tr('Target height, meters'),
            self.OBSERVER_POINTS))
        self.addParameter(ParameterTableField(
            self.SEARCH_RADIUS,
            self.tr('Search radius, meters'),
            self.OBSERVER_POINTS))
        self.addParameter(ParameterBoolean(
            self.USE_CURVATURE,
            self.tr('Take in account Earth curvature'),
            False))
        self.addParameter(ParameterNumber(
            self.REFRACTION,
            self.tr('Atmoshpheric refraction'),
            0.0, 1, 0.13))
        self.addParameter(ParameterSelection(
            self.PRECISION,
            self.tr('Algorithm precision'),
            self.PRECISIONS,
            1))
        self.addParameter(ParameterSelection(
            self.ANALYSIS_TYPE,
            self.tr('Analysis type'),
            self.TYPES,
            0))
        self.addParameter(ParameterBoolean(
            self.CUMULATIVE,
            self.tr('Generate cumulative output'),
            False))

        self.addOutput(OutputDirectory(
            self.OUTPUT,
            self.tr('Directory for storing results')))

    def processAlgorithm(self, feedback):
        dem = dataobjects.getObjectFromUri(
            self.getParameterValue(self.DEM))
        observer = dataobjects.getObjectFromUri(
            self.getParameterValue(self.OBSERVER_POINTS))
        observerIdField = self.getParameterValue(self.OBSERVER_ID)
        observerHeight = self.getParameterValue(self.OBSERVER_HEIGHT)
        targetHeight = self.getParameterValue(self.TARGET_HEIGHT)
        searchRadius = self.getParameterValue(self.SEARCH_RADIUS)
        useEarthCurvature = self.getParameterValue(self.USE_CURVATURE)
        refraction = self.getParameterValue(self.REFRACTION)
        precision = self.getParameterValue(self.PRECISION)
        analysisType = self.getParameterValue(self.ANALYSIS_TYPE)
        cumulative = self.getParameterValue(self.CUMULATIVE)

        outputPath = self.getOutputValue(self.OUTPUT)

        # convert meters to layer distance units
        coef = QgsUnitTypes.fromUnitToUnitFactor(Qgis.DistanceMeters, dem.crs().mapUnits())
        searchRadius = searchRadius * coef


        visibility.viewshed(dem,
                            observer,
                            observerIdField,
                            observerHeight,
                            targetHeight,
                            searchRadius,
                            useEarthCurvature,
                            refraction,
                            analysisType,
                            precision,
                            outputPath)