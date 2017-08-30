import os, ctypes
from ctypes import c_bool, c_char, c_char_p, c_int, c_uint, c_float, Structure, create_string_buffer, cast, pointer
class StartPos(Structure):
	_fields_ = [('x', c_int), ('y', c_int)]
	def __str__(self):
		return '(%i, %i)' % (self.x, self.y)
class MapInfo(Structure):
	def __init__(self):
		self.author = cast(create_string_buffer(200), c_char_p) # BUG: author field shows up as empty, probably something to do with the fact it's after the startpos structs
		self.description = cast(create_string_buffer(255), c_char_p)
		
	_fields_ = [('description', c_char_p),
			('tidalStrength', c_int),
			('gravity', c_int),
			('maxMetal', c_float),
			('extractorRadius', c_int),
			('minWind', c_int),
			('maxWind', c_int),
			('width', c_int),
			('height', c_int),
			('posCount', c_int),
			('StartPos', StartPos * 16),
			('author', c_char_p)]

class Unitsync:
	def __init__(self, location='.'):
		if location.endswith('.so'):
			self.unitsync = ctypes.cdll.LoadLibrary(location)
		elif location.endswith('.dll'): 
			locationdir = os.path.dirname(location)
			# load devil first, to avoid dll conflicts
			ctypes.windll.LoadLibrary(locationdir + "/devil.dll" )
			# load other dependencies, in case the spring dir is not in PATH
			ctypes.windll.LoadLibrary(locationdir + "/SDL2.dll" )
			self.unitsync = ctypes.windll.LoadLibrary(location)

		self.unitsync.GetNextError.restype = c_char_p
		self.unitsync.GetSpringVersion.restype = c_char_p
		self.unitsync.GetSpringVersionPatchset.restype = c_char_p
		self.unitsync.IsSpringReleaseVersion.restype = c_bool
		self.unitsync.Init.restype = c_int
		self.unitsync.GetWritableDataDirectory.restype = c_char_p
		self.unitsync.GetDataDirectoryCount.restype = c_int
		self.unitsync.GetDataDirectory.restype = c_char_p
		self.unitsync.ProcessUnits.restype = c_int
		self.unitsync.GetUnitCount.restype = c_int
		self.unitsync.GetUnitName.restype = c_char_p
		self.unitsync.GetFullUnitName.restype = c_char_p
		self.unitsync.GetArchiveChecksum.restype = c_uint
		self.unitsync.GetArchivePath.restype = c_char_p
		self.unitsync.GetMapCount.restype = c_int
		self.unitsync.GetMapInfoCount.restype = c_int
		self.unitsync.GetMapName.restype = c_char_p
		self.unitsync.GetMapFileName.restype = c_char_p
		self.unitsync.GetMapMinHeight.restype = c_float
		self.unitsync.GetMapMaxHeight.restype = c_float
		self.unitsync.GetMapArchiveCount.restype = c_int
		self.unitsync.GetMapArchiveName.restype = c_char_p
		self.unitsync.GetMapChecksum.restype = c_uint
		self.unitsync.GetMapChecksumFromName.restype = c_uint
		self.unitsync.GetMinimap.restype = pointer
		self.unitsync.GetInfoMapSize.restype = c_int
		self.unitsync.GetInfoMap.restype = c_int
		self.unitsync.GetSkirmishAICount.restype = c_int
		self.unitsync.GetSkirmishAIInfoCount.restype = c_int
		self.unitsync.GetInfoKey.restype = c_char_p
		self.unitsync.GetInfoType.restype = c_char_p
		self.unitsync.GetInfoValueString.restype = c_char_p
		self.unitsync.GetInfoValueInteger.restype = c_int
		self.unitsync.GetInfoValueFloat.restype = c_float
		self.unitsync.GetInfoValueBool.restype = c_bool
		self.unitsync.GetInfoDescription.restype = c_char_p
		self.unitsync.GetSkirmishAIOptionCount.restype = c_int
		self.unitsync.GetPrimaryModCount.restype = c_int
		self.unitsync.GetPrimaryModInfoCount.restype = c_int
		self.unitsync.GetPrimaryModArchive.restype = c_char_p
		self.unitsync.GetPrimaryModArchiveCount.restype = c_int
		self.unitsync.GetPrimaryModArchiveList.restype = c_char_p
		self.unitsync.GetPrimaryModIndex.restype = c_int
		self.unitsync.GetPrimaryModChecksum.restype = c_uint
		self.unitsync.GetPrimaryModChecksumFromName.restype = c_uint
		self.unitsync.GetSideCount.restype = c_int
		self.unitsync.GetSideName.restype = c_char_p
		self.unitsync.GetSideStartUnit.restype = c_char_p
		self.unitsync.GetMapOptionCount.restype = c_int
		self.unitsync.GetModOptionCount.restype = c_int
		self.unitsync.GetCustomOptionCount.restype = c_int
		self.unitsync.GetOptionKey.restype = c_char_p
		self.unitsync.GetOptionScope.restype = c_char_p
		self.unitsync.GetOptionName.restype = c_char_p
		self.unitsync.GetOptionSection.restype = c_char_p
		self.unitsync.GetOptionDesc.restype = c_char_p
		self.unitsync.GetOptionType.restype = c_int
		self.unitsync.GetOptionBoolDef.restype = c_int
		self.unitsync.GetOptionNumberDef.restype = c_float
		self.unitsync.GetOptionNumberMin.restype = c_float
		self.unitsync.GetOptionNumberMax.restype = c_float
		self.unitsync.GetOptionNumberStep.restype = c_float
		self.unitsync.GetOptionStringDef.restype = c_char_p
		self.unitsync.GetOptionStringMaxLen.restype = c_int
		self.unitsync.GetOptionListCount.restype = c_int
		self.unitsync.GetOptionListDef.restype = c_char_p
		self.unitsync.GetOptionListItemKey.restype = c_char_p
		self.unitsync.GetOptionListItemName.restype = c_char_p
		self.unitsync.GetOptionListItemDesc.restype = c_char_p
		self.unitsync.GetModValidMapCount.restype = c_int
		self.unitsync.GetModValidMap.restype = c_char_p
		self.unitsync.OpenFileVFS.restype = c_int
		self.unitsync.ReadFileVFS.restype = c_int
		self.unitsync.FileSizeVFS.restype = c_int
		self.unitsync.InitFindVFS.restype = c_int
		self.unitsync.InitDirListVFS.restype = c_int
		self.unitsync.InitSubDirsVFS.restype = c_int
		self.unitsync.FindFilesVFS.restype = c_int
		self.unitsync.OpenArchive.restype = c_int
		self.unitsync.FindFilesArchive.restype = c_int
		self.unitsync.OpenArchiveFile.restype = c_int
		self.unitsync.ReadArchiveFile.restype = c_int
		self.unitsync.SizeArchiveFile.restype = c_int
		self.unitsync.GetSpringConfigFile.restype = c_char_p
		self.unitsync.GetSpringConfigString.restype = c_char_p
		self.unitsync.GetSpringConfigInt.restype = c_int
		self.unitsync.GetSpringConfigFloat.restype = c_float
		self.unitsync.lpOpenFile.restype = c_int
		self.unitsync.lpOpenSource.restype = c_int
		self.unitsync.lpExecute.restype = c_int
		self.unitsync.lpErrorLog.restype = c_char_p
		self.unitsync.lpRootTable.restype = c_int
		self.unitsync.lpRootTableExpr.restype = c_int
		self.unitsync.lpSubTableInt.restype = c_int
		self.unitsync.lpSubTableStr.restype = c_int
		self.unitsync.lpSubTableExpr.restype = c_int
		self.unitsync.lpGetKeyExistsInt.restype = c_int
		self.unitsync.lpGetKeyExistsStr.restype = c_int
		self.unitsync.lpGetIntKeyType.restype = c_int
		self.unitsync.lpGetStrKeyType.restype = c_int
		self.unitsync.lpGetIntKeyListCount.restype = c_int
		self.unitsync.lpGetIntKeyListEntry.restype = c_int
		self.unitsync.lpGetStrKeyListCount.restype = c_int
		self.unitsync.lpGetStrKeyListEntry.restype = c_char_p
		self.unitsync.lpGetIntKeyIntVal.restype = c_int
		self.unitsync.lpGetStrKeyIntVal.restype = c_int
		self.unitsync.lpGetIntKeyBoolVal.restype = c_int
		self.unitsync.lpGetStrKeyBoolVal.restype = c_int
		self.unitsync.lpGetIntKeyFloatVal.restype = c_float
		self.unitsync.lpGetStrKeyFloatVal.restype = c_float
		self.unitsync.lpGetIntKeyStrVal.restype = c_char_p
		self.unitsync.lpGetStrKeyStrVal.restype = c_char_p

	def GetNextError(self): return self.unitsync.GetNextError()
	def GetSpringVersion(self): return self.unitsync.GetSpringVersion()
	def GetSpringVersionPatchset(self): return self.unitsync.GetSpringVersionPatchset()
	def IsSpringReleaseVersion(self): return self.unitsync.IsSpringReleaseVersion()
	def Init(self, isServer, id): return self.unitsync.Init(isServer, id)
	def UnInit(self): return self.unitsync.UnInit()
	def GetWritableDataDirectory(self): return self.unitsync.GetWritableDataDirectory()
	def GetDataDirectoryCount(self): return self.unitsync.GetDataDirectoryCount()
	def GetDataDirectory(self, index): return self.unitsync.GetDataDirectory(index)
	def ProcessUnits(self): return self.unitsync.ProcessUnits()
	def GetUnitCount(self): return self.unitsync.GetUnitCount()
	def GetUnitName(self, unit): return self.unitsync.GetUnitName(unit)
	def GetFullUnitName(self, unit): return self.unitsync.GetFullUnitName(unit)
	def AddArchive(self, archiveName): return self.unitsync.AddArchive(archiveName)
	def AddAllArchives(self, rootArchiveName): return self.unitsync.AddAllArchives(rootArchiveName)
	def RemoveAllArchives(self): return self.unitsync.RemoveAllArchives()
	def GetArchiveChecksum(self, archiveName): return self.unitsync.GetArchiveChecksum(archiveName)
	def GetArchivePath(self, archiveName): return self.unitsync.GetArchivePath(archiveName)
	def GetMapCount(self): return self.unitsync.GetMapCount()
	def GetMapInfoCount(self, index): return self.unitsync.GetMapInfoCount(index)
	def GetMapName(self, index): return self.unitsync.GetMapName(index)
	def GetMapFileName(self, index): return self.unitsync.GetMapFileName(index)
	def GetMapMinHeight(self, mapName): return self.unitsync.GetMapMinHeight(mapName)
	def GetMapMaxHeight(self, mapName): return self.unitsync.GetMapMaxHeight(mapName)
	def GetMapArchiveCount(self, mapName): return self.unitsync.GetMapArchiveCount(mapName)
	def GetMapArchiveName(self, index): return self.unitsync.GetMapArchiveName(index)
	def GetMapChecksum(self, index): return self.unitsync.GetMapChecksum(index)
	def GetMapChecksumFromName(self, mapName): return self.unitsync.GetMapChecksumFromName(mapName)
	def GetMinimap(self, fileName, mipLevel): return self.unitsync.GetMinimap(fileName, mipLevel)
	def GetInfoMapSize(self, mapName, name, width, height): return self.unitsync.GetInfoMapSize(mapName, name, width, height)
	def GetInfoMap(self, mapName, name, data, typeHint): return self.unitsync.GetInfoMap(mapName, name, pointer(char* data), typeHint)
	def GetSkirmishAICount(self): return self.unitsync.GetSkirmishAICount()
	def GetSkirmishAIInfoCount(self, index): return self.unitsync.GetSkirmishAIInfoCount(index)
	def GetInfoKey(self, index): return self.unitsync.GetInfoKey(index)
	def GetInfoType(self, index): return self.unitsync.GetInfoType(index)
	def GetInfoValueString(self, index): return self.unitsync.GetInfoValueString(index)
	def GetInfoValueInteger(self, index): return self.unitsync.GetInfoValueInteger(index)
	def GetInfoValueFloat(self, index): return self.unitsync.GetInfoValueFloat(index)
	def GetInfoValueBool(self, index): return self.unitsync.GetInfoValueBool(index)
	def GetInfoDescription(self, index): return self.unitsync.GetInfoDescription(index)
	def GetSkirmishAIOptionCount(self, index): return self.unitsync.GetSkirmishAIOptionCount(index)
	def GetPrimaryModCount(self): return self.unitsync.GetPrimaryModCount()
	def GetPrimaryModInfoCount(self, index): return self.unitsync.GetPrimaryModInfoCount(index)
	def GetPrimaryModArchive(self, index): return self.unitsync.GetPrimaryModArchive(index)
	def GetPrimaryModArchiveCount(self, index): return self.unitsync.GetPrimaryModArchiveCount(index)
	def GetPrimaryModArchiveList(self, archive): return self.unitsync.GetPrimaryModArchiveList(archive)
	def GetPrimaryModIndex(self, name): return self.unitsync.GetPrimaryModIndex(name)
	def GetPrimaryModChecksum(self, index): return self.unitsync.GetPrimaryModChecksum(index)
	def GetPrimaryModChecksumFromName(self, name): return self.unitsync.GetPrimaryModChecksumFromName(name)
	def GetSideCount(self): return self.unitsync.GetSideCount()
	def GetSideName(self, side): return self.unitsync.GetSideName(side)
	def GetSideStartUnit(self, side): return self.unitsync.GetSideStartUnit(side)
	def GetMapOptionCount(self, mapName): return self.unitsync.GetMapOptionCount(mapName)
	def GetModOptionCount(self): return self.unitsync.GetModOptionCount()
	def GetCustomOptionCount(self, fileName): return self.unitsync.GetCustomOptionCount(fileName)
	def GetOptionKey(self, optIndex): return self.unitsync.GetOptionKey(optIndex)
	def GetOptionScope(self, optIndex): return self.unitsync.GetOptionScope(optIndex)
	def GetOptionName(self, optIndex): return self.unitsync.GetOptionName(optIndex)
	def GetOptionSection(self, optIndex): return self.unitsync.GetOptionSection(optIndex)
	def GetOptionDesc(self, optIndex): return self.unitsync.GetOptionDesc(optIndex)
	def GetOptionType(self, optIndex): return self.unitsync.GetOptionType(optIndex)
	def GetOptionBoolDef(self, optIndex): return self.unitsync.GetOptionBoolDef(optIndex)
	def GetOptionNumberDef(self, optIndex): return self.unitsync.GetOptionNumberDef(optIndex)
	def GetOptionNumberMin(self, optIndex): return self.unitsync.GetOptionNumberMin(optIndex)
	def GetOptionNumberMax(self, optIndex): return self.unitsync.GetOptionNumberMax(optIndex)
	def GetOptionNumberStep(self, optIndex): return self.unitsync.GetOptionNumberStep(optIndex)
	def GetOptionStringDef(self, optIndex): return self.unitsync.GetOptionStringDef(optIndex)
	def GetOptionStringMaxLen(self, optIndex): return self.unitsync.GetOptionStringMaxLen(optIndex)
	def GetOptionListCount(self, optIndex): return self.unitsync.GetOptionListCount(optIndex)
	def GetOptionListDef(self, optIndex): return self.unitsync.GetOptionListDef(optIndex)
	def GetOptionListItemKey(self, optIndex, itemIndex): return self.unitsync.GetOptionListItemKey(optIndex, itemIndex)
	def GetOptionListItemName(self, optIndex, itemIndex): return self.unitsync.GetOptionListItemName(optIndex, itemIndex)
	def GetOptionListItemDesc(self, optIndex, itemIndex): return self.unitsync.GetOptionListItemDesc(optIndex, itemIndex)
	def GetModValidMapCount(self): return self.unitsync.GetModValidMapCount()
	def GetModValidMap(self, index): return self.unitsync.GetModValidMap(index)
	def OpenFileVFS(self, name): return self.unitsync.OpenFileVFS(name)
	def CloseFileVFS(self, file): return self.unitsync.CloseFileVFS(file)
	def ReadFileVFS(self, file, buf, numBytes): return self.unitsync.ReadFileVFS(file, pointer(char* buf), numBytes)
	def FileSizeVFS(self, file): return self.unitsync.FileSizeVFS(file)
	def InitFindVFS(self, pattern): return self.unitsync.InitFindVFS(pattern)
	def InitDirListVFS(self, path, pattern, modes): return self.unitsync.InitDirListVFS(path, pattern, modes)
	def InitSubDirsVFS(self, path, pattern, modes): return self.unitsync.InitSubDirsVFS(path, pattern, modes)
	def FindFilesVFS(self, file, nameBuf, size): return self.unitsync.FindFilesVFS(file, nameBuf, size)
	def OpenArchive(self, name): return self.unitsync.OpenArchive(name)
	def CloseArchive(self, archive): return self.unitsync.CloseArchive(archive)
	def FindFilesArchive(self, archive, file, nameBuf, size): return self.unitsync.FindFilesArchive(archive, file, nameBuf, size)
	def OpenArchiveFile(self, archive, name): return self.unitsync.OpenArchiveFile(archive, name)
	def ReadArchiveFile(self, archive, file, buffer, numBytes): return self.unitsync.ReadArchiveFile(archive, file, pointer(char* buffer), numBytes)
	def CloseArchiveFile(self, archive, file): return self.unitsync.CloseArchiveFile(archive, file)
	def SizeArchiveFile(self, archive, file): return self.unitsync.SizeArchiveFile(archive, file)
	def SetSpringConfigFile(self, fileNameAsAbsolutePath): return self.unitsync.SetSpringConfigFile(fileNameAsAbsolutePath)
	def GetSpringConfigFile(self): return self.unitsync.GetSpringConfigFile()
	def GetSpringConfigString(self, name, defValue): return self.unitsync.GetSpringConfigString(name, defValue)
	def GetSpringConfigInt(self, name, defValue): return self.unitsync.GetSpringConfigInt(name, defValue)
	def GetSpringConfigFloat(self, name, defValue): return self.unitsync.GetSpringConfigFloat(name, defValue)
	def SetSpringConfigString(self, name, value): return self.unitsync.SetSpringConfigString(name, value)
	def SetSpringConfigInt(self, name, value): return self.unitsync.SetSpringConfigInt(name, value)
	def SetSpringConfigFloat(self, name, value): return self.unitsync.SetSpringConfigFloat(name, value)
	def DeleteSpringConfigKey(self, name): return self.unitsync.DeleteSpringConfigKey(name)
	def lpClose(self): return self.unitsync.lpClose()
	def lpOpenFile(self, fileName, fileModes, accessModes): return self.unitsync.lpOpenFile(fileName, fileModes, accessModes)
	def lpOpenSource(self, source, accessModes): return self.unitsync.lpOpenSource(source, accessModes)
	def lpExecute(self): return self.unitsync.lpExecute()
	def lpErrorLog(self): return self.unitsync.lpErrorLog()
	def lpAddTableInt(self, key, override): return self.unitsync.lpAddTableInt(key, override)
	def lpAddTableStr(self, key, override): return self.unitsync.lpAddTableStr(key, override)
	def lpEndTable(self): return self.unitsync.lpEndTable()
	def lpAddIntKeyIntVal(self, key, value): return self.unitsync.lpAddIntKeyIntVal(key, value)
	def lpAddStrKeyIntVal(self, key, value): return self.unitsync.lpAddStrKeyIntVal(key, value)
	def lpAddIntKeyBoolVal(self, key, value): return self.unitsync.lpAddIntKeyBoolVal(key, value)
	def lpAddStrKeyBoolVal(self, key, value): return self.unitsync.lpAddStrKeyBoolVal(key, value)
	def lpAddIntKeyFloatVal(self, key, value): return self.unitsync.lpAddIntKeyFloatVal(key, value)
	def lpAddStrKeyFloatVal(self, key, value): return self.unitsync.lpAddStrKeyFloatVal(key, value)
	def lpAddIntKeyStrVal(self, key, value): return self.unitsync.lpAddIntKeyStrVal(key, value)
	def lpAddStrKeyStrVal(self, key, value): return self.unitsync.lpAddStrKeyStrVal(key, value)
	def lpRootTable(self): return self.unitsync.lpRootTable()
	def lpRootTableExpr(self, expr): return self.unitsync.lpRootTableExpr(expr)
	def lpSubTableInt(self, key): return self.unitsync.lpSubTableInt(key)
	def lpSubTableStr(self, key): return self.unitsync.lpSubTableStr(key)
	def lpSubTableExpr(self, expr): return self.unitsync.lpSubTableExpr(expr)
	def lpPopTable(self): return self.unitsync.lpPopTable()
	def lpGetKeyExistsInt(self, key): return self.unitsync.lpGetKeyExistsInt(key)
	def lpGetKeyExistsStr(self, key): return self.unitsync.lpGetKeyExistsStr(key)
	def lpGetIntKeyType(self, key): return self.unitsync.lpGetIntKeyType(key)
	def lpGetStrKeyType(self, key): return self.unitsync.lpGetStrKeyType(key)
	def lpGetIntKeyListCount(self): return self.unitsync.lpGetIntKeyListCount()
	def lpGetIntKeyListEntry(self, index): return self.unitsync.lpGetIntKeyListEntry(index)
	def lpGetStrKeyListCount(self): return self.unitsync.lpGetStrKeyListCount()
	def lpGetStrKeyListEntry(self, index): return self.unitsync.lpGetStrKeyListEntry(index)
	def lpGetIntKeyIntVal(self, key, defValue): return self.unitsync.lpGetIntKeyIntVal(key, defValue)
	def lpGetStrKeyIntVal(self, key, defValue): return self.unitsync.lpGetStrKeyIntVal(key, defValue)
	def lpGetIntKeyBoolVal(self, key, defValue): return self.unitsync.lpGetIntKeyBoolVal(key, defValue)
	def lpGetStrKeyBoolVal(self, key, defValue): return self.unitsync.lpGetStrKeyBoolVal(key, defValue)
	def lpGetIntKeyFloatVal(self, key, defValue): return self.unitsync.lpGetIntKeyFloatVal(key, defValue)
	def lpGetStrKeyFloatVal(self, key, defValue): return self.unitsync.lpGetStrKeyFloatVal(key, defValue)
	def lpGetIntKeyStrVal(self, key, defValue): return self.unitsync.lpGetIntKeyStrVal(key, defValue)
	def lpGetStrKeyStrVal(self, key, defValue): return self.unitsync.lpGetStrKeyStrVal(key, defValue)