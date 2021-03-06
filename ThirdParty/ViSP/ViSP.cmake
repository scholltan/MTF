option(WITH_VISP "Enable ViSP Template Trackers" ON)
if(WITH_VISP)
	find_package(VISP)
	if(VISP_FOUND)
		if (NOT WIN32)
			set(THIRD_PARTY_LIBS ${THIRD_PARTY_LIBS} -L/usr/local/lib/x86_64-linux-gnu)
		endif()
		set(THIRD_PARTY_LIBS ${THIRD_PARTY_LIBS} ${VISP_LIBRARIES})
		set(THIRD_PARTY_INCLUDE_DIRS ${THIRD_PARTY_INCLUDE_DIRS} ViSP/include)
		set(THIRD_PARTY_EXT_INCLUDE_DIRS ${THIRD_PARTY_EXT_INCLUDE_DIRS} ${VISP_INCLUDE_DIRS})
		set(THIRD_PARTY_TRACKERS ${THIRD_PARTY_TRACKERS} ViSP/src/ViSP)
		message(STATUS "Getting ViSP headers from: ${VISP_INCLUDE_DIRS}")
		message(STATUS "Using ViSP libraries: ${VISP_LIBRARIES}")
	else(VISP_FOUND)
		set(THIRD_PARTY_DEFINITIONS ${THIRD_PARTY_DEFINITIONS} DISABLE_VISP)
		message(STATUS "ViSP not found so its template tracker module cannot be enabled")
	endif(VISP_FOUND)	
else(WITH_VISP)		
	set(THIRD_PARTY_DEFINITIONS ${THIRD_PARTY_DEFINITIONS} DISABLE_VISP)
	message(STATUS "ViSP disabled")
	# message(STATUS "ViSP: THIRD_PARTY_RUNTIME_FLAGS: ${THIRD_PARTY_RUNTIME_FLAGS}")
endif(WITH_VISP)
