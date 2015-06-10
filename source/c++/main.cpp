#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

#ifdef _MSC_VER
# if CV_MAJOR_VERSION == 2 && CV_MINOR_VERSION == 4 && CV_SUBMINOR_VERSION == 10
// OpenCV 2.4.10
#  if defined(_DEBUG)
#  pragma comment(lib, "opencv_core2410d.lib")
#  pragma comment(lib, "opencv_highgui2410d.lib")
#  pragma comment(lib, "opencv_imgproc2410d.lib")
#  pragma comment(lib, "opencv_video2410d.lib")
#  pragma comment(lib, "opencv_ml2410d.lib")

#  pragma comment(lib, "opencv_calib3d2410d.lib")
#  pragma comment(lib, "opencv_objdetect2410d.lib")
#  pragma comment(lib, "opencv_features2d2410d.lib")
#  pragma comment(lib, "opencv_contrib2410d.lib")
#  pragma comment(lib, "opencv_ts2410d.lib")
#  pragma comment(lib, "opencv_legacy2410d.lib")
#  pragma comment(lib, "opencv_flann2410d.lib")
#  pragma comment(lib, "opencv_gpu2410d.lib")
# else
#  pragma comment(lib, "opencv_core2410.lib")
#  pragma comment(lib, "opencv_highgui2410.lib")
#  pragma comment(lib, "opencv_imgproc2410.lib")
#  pragma comment(lib, "opencv_video2410.lib")
#  pragma comment(lib, "opencv_ml2410.lib")

#  pragma comment(lib, "opencv_calib3d2410.lib")
#  pragma comment(lib, "opencv_objdetect2410.lib")
#  pragma comment(lib, "opencv_features2d2410.lib")
#  pragma comment(lib, "opencv_contrib2410.lib")
#  pragma comment(lib, "opencv_ts2410.lib")
#  pragma comment(lib, "opencv_legacy2410.lib")
#  pragma comment(lib, "opencv_flann2410.lib")
#  pragma comment(lib, "opencv_gpu2410.lib")
# endif //#  if defined(_DEBUG)

# endif //# if CV_MAJOR_VERSION == 2 && CV_MINOR_VERSION == 4 && CV_SUBMINOR_VERSION == 10
#endif //#ifdef _MSC_VER

string window_name = "Capture - Face detection";
RNG rng(12345);


int main(int argc, char* argv[])
{
	/*cout << "Debug: ";
	for (int i(0); i < argc; i++)
	{
		cout << " " << argv[i];
	}
	cout << endl;*/

	if (argc < 8) return -1;

	String image_name        = argv[1];
	String cascade_name      = argv[2];
	double scale_factor = atof(argv[3]);
	int min_neighbors   = atoi(argv[4]);
	int flags           = atoi(argv[5]);
	int min_size_x      = atoi(argv[6]);
	int min_size_y      = atoi(argv[7]);
	int max_size_x      = atoi(argv[8]);
	int max_size_y      = atoi(argv[9]);

	bool nested_object = (bool)atoi(argv[10]);

	String cascade_name2;
	double scale_factor2;
	int min_neighbors2;
	int flags2;
	int min_size_x2;
	int min_size_y2;
	int max_size_x2;
	int max_size_y2;
	CascadeClassifier cascade2;
	std::vector<Rect> objects2;
	if (nested_object)
	{
		cascade_name2	 = argv[11];
		scale_factor2	 = atof(argv[12]);
		min_neighbors2   = atoi(argv[13]);
		flags2           = atoi(argv[14]);
		min_size_x2      = atoi(argv[15]);
		min_size_y2      = atoi(argv[16]);
		max_size_x2      = atoi(argv[17]);
		max_size_y2      = atoi(argv[18]);
	}

	CascadeClassifier cascade;

	int rows;
	int cols;
	int long_edge = 1000;
    Mat img = cv::imread(image_name);

	if (img.rows > img.cols)
	{
		rows = long_edge;
		cols = rows*img.cols/img.rows;
	}
	else
	{
		cols = long_edge;
		rows = cols*img.rows/img.cols;
	}

	cv::resize(img, img, Size(cols, rows));

	   //-- 1. Load the cascade
	if( !cascade.load( cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };
	if (nested_object)
	{
		if( !cascade2.load( cascade_name2 ) ){ printf("--(!)Error loading\n"); return -1; };
	}
	std::vector<Rect> objects;
	Mat frame_gray;

	cvtColor(img, frame_gray, CV_BGR2GRAY);
	equalizeHist(frame_gray, frame_gray);

	//-- Detect objects
	if (min_size_x <= 0 || min_size_y <= 0)
		cascade.detectMultiScale(frame_gray, objects, scale_factor, min_neighbors, flags);
	else if (max_size_x > 0 && max_size_y > 0 && max_size_x > min_size_x && max_size_y > min_size_y)
		cascade.detectMultiScale(frame_gray, objects, scale_factor, min_neighbors, flags, Size(min_size_x, min_size_y), Size(max_size_x, max_size_y));
	else
		cascade.detectMultiScale(frame_gray, objects, scale_factor, min_neighbors, flags, Size(min_size_x, min_size_y));

	if (nested_object)
	{
		for( size_t i = 0; i < objects.size(); i++ )
		{
			Mat objectROI = frame_gray( objects[i] );

			//-- In each object, detect nested object
			if (min_size_x2 <= 0 || min_size_y2 <= 0)
				cascade2.detectMultiScale(objectROI, objects2, scale_factor2, min_neighbors2, flags2);
			else if (max_size_x2 > 0 && max_size_y2 > 0 && max_size_x2 > min_size_x2 && max_size_y2 > min_size_y2)
				cascade2.detectMultiScale(objectROI, objects2, scale_factor2, min_neighbors2, flags2, Size(min_size_x2, min_size_y2), Size(max_size_x2, max_size_y2));
			else
				cascade2.detectMultiScale(objectROI, objects2, scale_factor2, min_neighbors2, flags2, Size(min_size_x2, min_size_y2));

		}
	}

	cout << "Found " << objects.size() << " objects" << " and " << objects2.size() << " nested objects";
	/*
	for( size_t i = 0; i < objects.size(); i++ )
    {
		Point center(objects[i].x + objects[i].width/2, objects[i].y + objects[i].height/2);
		ellipse(img, center, Size( objects[i].width/2, objects[i].height/2), 0, 0, 360, Scalar( 0, 255, 0 ), 2, 8, 0);
		if (nested_object)
		{
			for( size_t j = 0; j < objects2.size(); j++ )
			{
				Point center(objects[i].x + objects2[j].x + objects2[i].width/2, objects[i].y + objects2[j].y + objects2[j].height/2);
				ellipse(img, center, Size( objects2[j].width/2, objects2[j].height/2), 0, 0, 360, Scalar( 255, 0, 0 ), 2, 8, 0);
			}
		}
	}


	cv::imshow("img", img);
    cv::waitKey(0);	*/
	return 0;
}


