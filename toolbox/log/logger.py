from typing import Optional, Any, Dict, Tuple, Union
import os
import numpy as np
import datetime
from ..printing import print_color, debug, sdebug, ldebug, warn

class Logger:
    """
    This class is used to log all sorts of infos depending on the parameters given to the class.
    - If verbose is True, then the logger will print all the infos given to it.
    - If save is True, then the logger will save all the infos given to it in a file (save_path).
    - if tensorboard is True, then the logger will save all the infos given to it in a tensorboard file (tensorboard_path).
    """

    def __init__(self, verbose: bool = False, save: bool = True, save_path: str = "logs", tensorboard: bool = False):
        self.verbose: bool = verbose
        self.save: bool = save
        self.save_path: str = save_path
        self.tensorboard: bool = tensorboard
        self.writer: Optional[Any] = None
        self.log_file: Optional[Any] = None
        self.log_counter: int = 0
        self.debug_counter: int = 0
        self.indexes: Dict[Tuple[str, str], int] = {} # Associates (log_type, log_name) to an index
        # Add current datetime to the save path
        self.save_path = os.path.join(self.save_path, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

        if self.save or self.tensorboard:
            assert self.save_path is not None, "save_path cannot be None if save is True or tensorboard is True"
            # Creates the directory if it does not exist
            debug(self.save_path)
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
                if verbose: print_color("Created directory " + os.path.dirname(self.save_path), "green")
            # Creates a log file (overwrites it if it already exists)
            log_file_path = os.path.join(self.save_path, "log.txt")
            self.log_file = open(log_file_path, "w")
            self.log_file.write("")
            if verbose: print_color("Created log file " + log_file_path, "green")

        if self.tensorboard:
            try:
                from torch.utils.tensorboard import SummaryWriter
                self.writer = SummaryWriter(log_dir=self.save_path)
                if verbose: print_color("Created tensorboard writer", "green")
                # Gives instruction on how to use tensorboard
                print_color("To use tensorboard, run the following command in a terminal:", "bold")
                print_color("tensorboard --logdir=" + self.save_path, "bold")
                print_color("Then open the following link in a browser:", "bold")
                print_color("http://localhost:6006/", "bold")
            except ImportError:
                raise ImportError("Please install tensorboard to use it")
        
    def log(self, message: str, verbose: Optional[bool] = None, color: Optional[str] = None) -> None:
        """
        Logs a message depending on the parameters given to the function.
        """
        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        if _verbose:
            print_color("(Log) " + message, color)
        if self.save:
            self.log_file.write("(Log) " + message + "\n")
        if self.tensorboard:
            self.writer.add_text("log", message, self.log_counter)
            self.log_counter += 1

    def log_dict(self, dictionary: dict, verbose: Optional[bool] = None, color: Optional[str] = None) -> None:
        """
        Logs a dictionary depending on the parameters given to the function.
        """
        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        if _verbose:
            print_color("(Log) " + str(dictionary), color)
        if self.save:
            self.log_file.write("(Log) " + str(dictionary) + "\n")
        if self.tensorboard:
            self.writer.add_text("log", str(dictionary), self.log_counter)
            self.log_counter += 1

    def log_value(self, name: str, value: float, index: Optional[int] = None, verbose: Optional[bool] = None, color: Optional[str] = None) -> None:
        """
        Logs a numerical value associated a metric name.
        The index is either specified by the user or automatically incremented.
        verbose permits to override the verbose parameter of the class.
        """
        # Saves the index
        key = ("value", name)
        if key not in self.indexes: self.indexes[key] = -1
        if index is None:
            index = self.indexes[key] + 1
        self.indexes[key] = index

        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        if _verbose:
            print_color(f"(Value) {name} - {index}: {value}", color)
        if self.save:
            self.log_file.write(f"(Value) {name} - {index}: {value}\n")
        if self.tensorboard:
            self.writer.add_scalar(name, value, index)

    def _log_image_torch(self, name: str, image: Any, images_path: str, index: int) -> None:
        return self._log_image_numpy(name, image.cpu().numpy(), images_path, index)
    
    def _log_image_numpy(self, name: str, image: Any, images_path: str, index: int) -> None:
        """
        Logs an image depending on the parameters given to the function.
        """
        # Reshape image if needed
        if len(image.shape) == 4: # Batch of images
            image = image[0]
            warn(f"(Image) {name} - {index}: Image is a batch of images, only the first one will be saved")
        if len(image.shape) == 3: # Image with channels
            # First figure out if we are in HWC or CHW
            # We don't know the dim of C, it could be 1 (grayscale) or 3 (RGB) or more (RGBA, RGBD, etc.)
            # We always output HWC with shape (H, W, 3) (so we convert grayscales, and RGBA to RGB)
            min_dim = np.argmin(image.shape) # We assume this is the channel dim
            if min_dim == 0: # CHW -> HWC
                image = np.transpose(image, (1, 2, 0))
            C = image.shape[2]
            if C == 1: # Grayscale
                image = np.repeat(image, 3, axis=2)
            elif C == 4: # RGBA, RGBD
                image = image[:, :, :3]
            elif C > 4: # Too many channels
                image = image[:, :, :3]
                warn(f"(Image) {name} - {index}: Image has {C} channels, only the first 3 will be saved")
        elif len(image.shape) == 2: # Grayscale image
            image = np.repeat(image[:, :, np.newaxis], 3, axis=2)
        else:
            raise ValueError(f"Image has {len(image.shape)} dimensions, only 2 or 3 are supported")

        if self.save:
            try:
                from PIL import Image
                # Saves the image
                image_path = os.path.join(images_path, name + "_" + str(index) + ".png")
                image_PIL = Image.fromarray((255 *image).astype(np.uint8))
                image_PIL.save(image_path)
            except ImportError:
                warn("Please install PIL to save images")
        if self.tensorboard:
            self.writer.add_image(name, image, index, dataformats="HWC")

    def _log_image_PIL(self, name: str, image: Any, images_path: str, index: int) -> None:
        """
        Logs an image depending on the parameters given to the function.
        """
        if self.save:
            image_path = os.path.join(images_path, name + "_" + str(index) + ".png")
            image.save(image_path)
        if self.tensorboard:
            # Convert PIL image to numpy array
            image_np = np.array(image)
            # Shape must be (H, W, C)
            if len(image_np.shape) == 2: # Grayscale image
                image_np = np.repeat(image_np[:, :, np.newaxis], 3, axis=2)
            # Go from 0-255 int to 0-1 float
            image_np = image_np.astype(np.float32) / 255
            self.writer.add_image(name, image_np, index, dataformats="HWC")

    def log_image(self, name: str, image: Any, index: Optional[int] = None, verbose: Optional[bool] = None, color: Optional[str] = None) -> None:
        """
        Logs an image depending on the parameters given to the function.
        """
        # Saves the index
        key = ("image", name)
        if key not in self.indexes: self.indexes[key] = -1
        if index is None:
            index = self.indexes[key] + 1
        self.indexes[key] = index

        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        if _verbose and not self.save and not self.tensorboard:
            warn(f"(Image) {name} - {index}: Not saved as save and tensorboard are False")
        images_path = os.path.join(self.save_path, "images")
        if self.save:
            # Save the image in the save_path/images folder
            # First, creates the directory if it does not exist
            if not os.path.exists(images_path):
                os.makedirs(images_path)
                if _verbose: print_color("(Image) Created directory " + os.path.dirname(images_path), ["green", "bold"])

        # Call the correct function depending on the type of image
        logged = False
        if isinstance(image, np.ndarray):
            self._log_image_numpy(name, image, images_path, index)
            logged = True
        else:
            try:
                from PIL import Image
                if isinstance(image, Image.Image):
                    self._log_image_PIL(name, image, images_path, index)
                    logged = True
            except ImportError:
                pass
            if not logged:
                try:
                    import torch
                    if isinstance(image, torch.Tensor):
                        self._log_image_torch(name, image, images_path, index)
                        logged = True
                except ImportError:
                    pass
        if not logged:
            raise ValueError(f"Image type {type(image)} not supported or the library is not installed")

        # Log confirmation
        if _verbose:
            if self.save:
                print_color(f"(Image) {name} - {index}: Saved in {images_path}", color)
            if self.tensorboard:
                print_color(f"(Image) {name} - {index}: Logged in tensorboard", color)
        if self.save:
            self.log_file.write(f"(Image) {name} - {index}: Saved in {images_path}\n")

    def log_histogram(self, name: str, values: np.ndarray, index: Optional[int] = None, verbose: Optional[bool] = None, color: Optional[str] = None) -> None:
        """
        Logs an histogram depending on the parameters given to the function.
        """
        # Saves the index
        key = ("histogram", name)
        if key not in self.indexes: self.indexes[key] = -1
        if index is None:
            index = self.indexes[key] + 1
        self.indexes[key] = index

        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        if _verbose and not self.save and not self.tensorboard:
            warn(f"(Histogram) {name} - {index}: Not saved as save and tensorboard are False")
        if self.save:
            # Save the histogram in the save_path/histograms folder
            # First, creates the directory if it does not exist
            histograms_dir = os.path.join(self.save_path, "histograms")
            if not os.path.exists(histograms_dir):
                os.makedirs(histograms_dir)
                if _verbose: print_color("(Histogram) Created directory " + histograms_dir, ["green", "bold"])
            # Then, saves the histogram
            histogram_path = os.path.join(histograms_dir, f"{name}_{index}.npy")
            np.save(histogram_path, values)
            if _verbose: print_color(f"(Histogram) Saved at {histogram_path}", color)
            # Finally, logs the histogram path
            self.log_file.write(f"(Histogram) {name} - {index}: Saved at {histogram_path}\n")
        if self.tensorboard:
            self.writer.add_histogram(name, values, index)
            if _verbose: print_color(f"(Histogram) Logged {name} - {index}", color)

    def log_graph(self, model: Any, input_size: Tuple[int, ...], verbose: bool = False, color: Optional[str] = None) -> None:
        """
        Logs a graph depending on the parameters given to the function.
        """
        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        if _verbose and not self.tensorboard:
            warn("(Graph) Graphs can only be displayed in tensorboard.")
        elif self.tensorboard:
            try:
                import torch
                self.writer.add_graph(model, torch.zeros(input_size))
                if _verbose: print_color("(Graph) Logged graph to tensorboard", color)
                if self.save: self.log_file.write("(Graph) Logged graph to tensorboard\n")
            except ImportError:
                raise ImportError("Please install torch to log graphs")
        elif self.save:
            self.log_file.write("(Graph) Graphs can only be displayed in tensorboard.\n")

    def save_model(self, model: Any, index: Union[str,int], verbose: Optional[bool] = None, color: Optional[str] = None) -> None:
        """
        Saves a model
        """
        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        if _verbose and not self.save:
            warn("(Model) Models can only be saved if save is True.")
        elif self.save:
            try:
                import torch
                # Save the model in the save_path/models folder
                # First, creates the directory if it does not exist
                models_dir = os.path.join(self.save_path, "models")
                if not os.path.exists(models_dir):
                    os.makedirs(models_dir)
                    if _verbose: print_color("(Model) Created directory " + models_dir, ["green", "bold"])
                # Then, saves the model
                model_path = os.path.join(models_dir, f"model_{index}.pt")
                torch.save(model.state_dict(), model_path)
                if _verbose: print_color(f"(Model) Saved at {model_path}", color)
                # Finally, logs the model path
                self.log_file.write(f"(Model) {index}: Saved at {model_path}\n")
            except ImportError:
                raise ImportError("Please install torch to save models")
            
    def debug(self, var: Any, verbose: bool = False, visible: bool = False) -> None:
        """
        Nested call to debug, to handle saving and tensorboard
        """
        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        debug_str = debug(var, visible=visible, return_str=True, display=_verbose, nested_calls=1)
        if self.save:
            self.log_file.write(debug_str + "\n")
        if self.tensorboard:
            self.writer.add_text("debug", debug_str.replace("DEBUG: ", ""), self.debug_counter)
            self.debug_counter += 1

    def sdebug(self, var: Any, verbose: bool = False, visible: bool = False) -> None:
        """
        Nested call to sdebug to handle saving and tensorboard
        """
        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        debug_str = sdebug(var, visible=visible, return_str=True, display=_verbose, nested_calls=1)
        if self.save:
            self.log_file.write(debug_str + "\n")
        if self.tensorboard:
            self.writer.add_text("debug", debug_str.replace("DEBUG: ", ""), self.debug_counter)
            self.debug_counter += 1

    def ldebug(self, var: Any, verbose: bool = False, visible: bool = False) -> None:
        """
        Nested call to ldebug to handle saving and tensorboard
        """
        _verbose = (verbose is not None and verbose) or (verbose is None and self.verbose)
        debug_str = ldebug(var, visible=visible, return_str=True, display=_verbose, nested_calls=1)
        if self.save:
            self.log_file.write(debug_str + "\n")
        if self.tensorboard:
            self.writer.add_text("debug", debug_str.replace("DEBUG: ", ""), self.debug_counter)
            self.debug_counter += 1
                          
        

