#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

#define TRACELN(text) std::cout << "face_detect: " << text << std::endl
template<typename T>
T stringTo(const string &text)
{
    std::istringstream ss(text);
    ss.flags(std::ios_base::skipws);
    T result;
    ss >> result;

    if (ss.fail() && ss.bad()) throw std::invalid_argument(text.c_str());

    return result;
}

class ImgObj {
    public:
        String image_name, cascade_name;
        double scale_factor;
        int min_neighbors, flags, min_size_x, max_size_x, min_size_y, max_size_y;

        template<class iterator_type>
        inline ImgObj(iterator_type args_it) {
            init(args_it);
        }

        template<class iterator_type>
        void  init(iterator_type args_it) {
            image_name     = *args_it++;
            cascade_name   = *args_it++;
            scale_factor   = stringTo<double>(*args_it++);
            min_neighbors  = stringTo<int>(*args_it++);
            flags          = stringTo<int>(*args_it++);
            min_size_x     = stringTo<int>(*args_it++);
            min_size_y     = stringTo<int>(*args_it++);
            max_size_x     = stringTo<int>(*args_it++);
            max_size_y     = stringTo<int>(*args_it);
        }

        inline string toString() {
            const auto tab = "    ";
            std::stringstream ss;
            ss << "Image:" << endl
               << tab << "name:          " << image_name << endl
               << tab << "cascade name:  " << cascade_name << endl
               << tab << "scale factor:  " << scale_factor << endl
               << tab << "min_neighbors: " << min_neighbors << endl
               << tab << "flags:         " << flags << endl
               << tab << "min x:         " << min_size_x << endl
               << tab << "min y:         " << min_size_y << endl
               << tab << "max x:         " << max_size_x << endl
               << tab << "max y:         " << max_size_y << endl;

            return ss.str();
        }
};

static inline void detectObjects(CascadeClassifier &cascade, const ImgObj &imgObj, vector<Rect> &objects, Mat &frame_gray) {
    if (imgObj.min_size_x <= 0 || imgObj.min_size_y <= 0)
        cascade.detectMultiScale(frame_gray, objects, imgObj.scale_factor, imgObj.min_neighbors, imgObj.flags);
    else if (imgObj.max_size_x > 0 && imgObj.max_size_y > 0 && imgObj.max_size_x > imgObj.min_size_x && imgObj.max_size_y > imgObj.min_size_y)
        cascade.detectMultiScale(frame_gray, objects, imgObj.scale_factor, imgObj.min_neighbors, imgObj.flags, Size(imgObj.min_size_x, imgObj.min_size_y), Size(imgObj.max_size_x, imgObj.max_size_y));
    else
        cascade.detectMultiScale(frame_gray, objects, imgObj.scale_factor, imgObj.min_neighbors, imgObj.flags, Size(imgObj.min_size_x, imgObj.min_size_y));
}

int main(int argc, char* argv[])
{
    if (argc < 8) {
        TRACELN("insufficient number of arguments");
        return -1;
    }

    CascadeClassifier cascade;
    Mat frame_gray;
    std::vector<Rect> objects, objects2;
    vector<string> args(argv + 1, argv + argc);

    auto imgObj = ImgObj(args.begin());

#define LONG_EDGE 1000
    int rows = LONG_EDGE, cols = LONG_EDGE;
    Mat img = cv::imread(imgObj.image_name);

    img.rows > img.cols ? cols = rows * img.cols / img.rows
                        : rows = cols * img.rows / img.cols;

    cv::resize(img, img, Size(cols, rows));
#undef LONG_EDGE

    if (!cascade.load(imgObj.cascade_name)) {
        TRACELN("--(!)Error loading main image");
        return -1;
    }

    cvtColor(img, frame_gray, CV_BGR2GRAY);
    equalizeHist(frame_gray, frame_gray);

    detectObjects(cascade, imgObj, objects, frame_gray);

    if (stringTo<bool>(args[9])) {
        CascadeClassifier cascade2;

        if (!cascade2.load(imgObj.cascade_name)) {
            TRACELN("--(!)Error loading nested image");
            return -1;
        }

        imgObj.init(args.begin() + 11);

        for (auto object : objects) {
            Mat objectROI = frame_gray(object);

            detectObjects(cascade2, imgObj, objects2, objectROI);
        }
    }

    TRACELN("Found " << objects.size() << " objects" << " and " << objects2.size() << " nested objects");
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
    cv::waitKey(0);    */
    return 0;
}


